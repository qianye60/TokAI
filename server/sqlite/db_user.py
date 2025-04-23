from sqlmodel import select
from sqlalchemy.orm import selectinload
from .dbconfig import get_session
from model.user_model import User, UserDB, UpdateUser
from model.chat_model import ChatDB
from fastapi import status, HTTPException
from tools.token import get_password_hash
from uuid import uuid4
from .db_config import get_config

default_M = 0

# 数据库操作函数
async def get_user(username: str) -> User | None:
    """根据用户名获取用户"""
    session = next(get_session())#迭代器接收数据库会话
    try:
        # 使用 selectinload 预加载所有关联数据
        statement = select(User).where(User.username == username).options(
            selectinload(User.chats).selectinload(ChatDB.messages)
        )
        user = session.exec(statement).first()
        if not user:
            return None
        session.refresh(user)
        return user
    except Exception as e:
        print(f"获取用户出错: {str(e)}")
        return None
    finally:
        session.close()

async def get_users() -> User | None:
    """获取所有用户"""
    session = next(get_session())#迭代器接收数据库会话
    try:
        users = session.exec(select(User)).all()
        return users
    except Exception as e:
        print(f"获取用户出错: {str(e)}")
        return None
    finally:
        session.close()

async def get_user_by_id(user_id: int) -> User | None:
    """根据用户ID获取用户"""
    session = next(get_session())
    try:
        user = session.exec(select(User).where(User.id == user_id)).first()
        return user
    except Exception as e:
        print(f"获取用户出错: {str(e)}")
        return None
    finally:
        session.close()

async def create_user(user:UserDB) -> str | bool :
    """创建用户"""
    session = next(get_session())
    try:
        # 检查用户名是否存在
        username_exists = session.exec(select(User).where(User.username == user.username)).first()
        if username_exists:
            return "1"
        
        # 检查邮箱是否存在
        email_exists = session.exec(select(User).where(User.email == user.email)).first()
        if email_exists:
            return "2"
        
        # 获取系统配置中的默认余额
        config = await get_config()
        default_money = config.default_money if config and config.default_money is not None else default_M
        
        # 创建新用户
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            money=default_money,
            userauth=0
        )
        session.add(db_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        session.close()

async def update_user_by_id(user_id: int, update_data:UpdateUser) -> User | None:
    """根据用户ID更新用户信息"""
    session = next(get_session())
    try:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return None
            
        # 保护超级管理员权限不被更改
        if user.userauth == 2 and update_data.userauth is not None and update_data.userauth != 2:
            raise HTTPException(status_code=403, detail="Cannot change super admin privileges")
            
        if update_data.username:
            # 检查用户名是否已被其他用户使用
            if user.username != update_data.username:
                username_exists = session.exec(select(User).where(
                    User.username == update_data.username, 
                    User.id != user_id
                )).first()
                if username_exists:
                    raise HTTPException(status_code=400, detail="用户名已被使用")
            user.username = update_data.username
            
        if update_data.email:
            user.email = update_data.email
            
        if update_data.password:
            user.hashed_password = get_password_hash(update_data.password)
            
        if update_data.money is not None:
            user.money = update_data.money
            
        if update_data.userauth is not None:
            # 任何人都不能被设置为超级管理员，并且现有超管不能被降级
            if update_data.userauth != 2 and user.userauth != 2:
                user.userauth = update_data.userauth
                
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        session.close()

async def delete_user_by_id(user_id: int):
    """根据用户ID删除用户"""
    from fastapi import HTTPException, status
    from model.chat_model import ChatDB, ChatMessageDB, chatConfig
    
    session = next(get_session())
    try:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return False
        elif user.userauth != 2:
            # 收集用户名以删除相关记录
            username = user.username
            
            # 1. 先删除用户的聊天消息
            chats = session.exec(select(ChatDB).where(ChatDB.username == username)).all()
            
            # 删除所有相关的消息
            for chat in chats:
                messages = session.exec(select(ChatMessageDB).where(ChatMessageDB.chat_id == chat.id)).all()
                for message in messages:
                    session.delete(message)
                # 删除对话
                session.delete(chat)
            
            # 2. 删除用户的聊天配置
            configs = session.exec(select(chatConfig).where(chatConfig.username == username)).all()
            for config in configs:
                session.delete(config)
            
            # 3. 最后删除用户本身
            session.delete(user)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        session.close()
