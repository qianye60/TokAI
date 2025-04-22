from sqlmodel import select
from fastapi import HTTPException
from sqlite.dbconfig import get_session
from model.chat_model import (ChatDB, Create_chat, Delete_chat, Update_chat,
                        Create_message, ChatMessageDB, Update_message,
                        Delete_message)
from datetime import datetime


#对话
async def create_chat(Chat: Create_chat):
    session = next(get_session())
    try:
        # 创建新聊天
        chat = ChatDB(
            title=Chat.title,
            createdAt=datetime.now(),
            username=Chat.username  # 使用username作为外键
        )
        
        session.add(chat)
        session.commit()
        session.refresh(chat)
        
        return chat
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_chat(Chat: Delete_chat):
    session = next(get_session())
    try:
        # 查找要删除的聊天记录
        chat = session.exec(select(ChatDB).where(ChatDB.id == Chat.conversationId)).first()
        if not chat:
            raise HTTPException(status_code=404, detail="聊天记录不存在")
            
        # 删除所有关联的消息
        for message in chat.messages:
            session.delete(message)
            
        # 删除聊天记录
        session.delete(chat)
        session.commit()
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

async def update_chat(Chat:Update_chat):
    session = next(get_session())
    try:
        chat = session.exec(select(ChatDB).where(ChatDB.id == Chat.conversationId)).one()
        chat.title = Chat.newtitle
        session.add(chat)
        session.commit()
        session.refresh(chat)
        
        return {"message": "更新成功"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))



#信息
async def create_message(Message: Create_message):
    session = next(get_session())
    try:
        message = ChatMessageDB(
            username=Message.username,
            content=Message.message,
            isuser=Message.isuser,
            chat_id=Message.conversationId
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        
        return message
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def update_message(Message: Update_message):
    session = next(get_session())
    try:
        message = session.exec(select(ChatMessageDB).where(ChatMessageDB.id == Message.messageId)).first()
        message.content = Message.message
        session.add(message)
        session.commit()
        session.refresh(message)
        
        return message
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def delete_message(Message:Delete_message):
    session = next(get_session())
    try:
        message = session.exec(select(ChatMessageDB).where(ChatMessageDB.id == Message.messageId)).first()
        session.delete(message)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
#一键删除全部
async def delete_all(username:Delete_message):
    session = next(get_session())
    try:
        # 查询所有聊天
        chats = session.exec(select(ChatDB).where(ChatDB.username == username.username)).all()
        
        # 遍历删除
        for chat in chats:
            # 删除所有关联的消息
            for message in chat.messages:
                session.delete(message)
            # 删除聊天记录
            session.delete(chat)
            
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))