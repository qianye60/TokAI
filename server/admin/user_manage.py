from fastapi import APIRouter, Depends, HTTPException, status
from tools.token import oauth2_scheme, get_password_hash
from sqlite.db_user import get_users, update_user_by_id, get_user_by_id, delete_user_by_id, create_user, get_user
from sqlite.db_config import get_config
from user.user import verify_token
from typing import Annotated, List
from model.user_model import User, Userinfo, UpdateUser, UserDB

user = APIRouter()

@user.get("/default-money")
async def get_default_money(token: Annotated[str, Depends(oauth2_scheme)]):
    """获取默认用户余额配置"""
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    elif user["userauth"] == 1 or user["userauth"] == 2:
        # 获取系统配置
        config = await get_config()
        return {"default_money": config.default_money}
    else:
        raise HTTPException(status_code=401, detail="Invalid token!")

@user.get("/users", response_model=List[Userinfo])
async def users(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    elif user["userauth"] == 1 or user["userauth"] == 2:
        users_list:List[User] = await get_users()
        # 转换为Userinfo对象列表，不包含敏感信息如密码哈希
        safe_users = [
            Userinfo(
                id=user.id,
                username=user.username,
                email=user.email,
                money=user.money,
                userauth=user.userauth
            ) for user in users_list
        ]
        return safe_users
    else:
        raise HTTPException(status_code=401, detail="Invalid token!")

#user_id 被更新用户的id  user_data 被更新用户的新数据 token 用户权限
@user.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UpdateUser, token: Annotated[str, Depends(oauth2_scheme)]):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    elif user["userauth"] == 1 or user["userauth"] == 2:
        # 检查是否试图修改超级管理员
        target_user = await get_user_by_id(user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        if target_user.userauth == 2:
            # 检查是否试图降级超级管理员
            if user_data.userauth is not None and user_data.userauth != 2:
                raise HTTPException(status_code=403, detail="不能修改超级管理员权限")
        # 检查是否试图修改管理员
        if user["userauth"] == 1 and (user_data.userauth == 2 or user_data.userauth == 1):
            raise HTTPException(status_code=403, detail="不能修改管理员权限")

        updated_user = await update_user_by_id(user_id, user_data)
        if updated_user:
            return {"message": "用户更新成功"}
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    else:
        raise HTTPException(status_code=401, detail="Invalid token!")


@user.delete("/users/{user_id}")
async def delete_user(user_id: int, token: Annotated[str, Depends(verify_token)]):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token!")
    elif token["userauth"] == 2:
        deleted_user = await delete_user_by_id(user_id)
        if deleted_user:
            return {"message": "用户删除成功"}
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    else:
        raise HTTPException(status_code=401, detail="Invalid token!")

@user.post("/users")
async def admin_create_user(
    user_data: dict, 
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """管理员创建用户"""
    current_user = await verify_token(token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    elif current_user["userauth"] == 1 or current_user["userauth"] == 2:
        try:
            # 验证必要字段
            if not user_data.get("username") or not user_data.get("email") or not user_data.get("password"):
                raise HTTPException(status_code=400, detail="缺少必要的用户信息")
            
            # 准备用户数据
            new_user = UserDB(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"])
            )
            
            # 创建用户
            result = await create_user(new_user)
            
            if result == "1":
                raise HTTPException(status_code=400, detail="用户名已存在")
            elif result == "2":
                raise HTTPException(status_code=400, detail="邮箱已存在")
            elif result is True:
                # 创建成功后，如果需要设置特定的余额或权限，再更新用户
                created_user = await get_user(user_data["username"])
                if created_user:
                    update_data = UpdateUser()
                    
                    # 仅超级管理员可以设置管理员权限
                    if "userauth" in user_data and user_data["userauth"] != 0:
                        if current_user["userauth"] == 2:  # 只有超级管理员
                            update_data.userauth = user_data["userauth"]
                    
                    # 设置余额（如果提供）
                    if "money" in user_data and user_data["money"] is not None:
                        update_data.money = user_data["money"]
                    
                    # 如果有需要更新的数据，则进行更新
                    if update_data.userauth is not None or update_data.money is not None:
                        await update_user_by_id(created_user.id, update_data)
                
                return {"message": "用户创建成功"}
            else:
                raise HTTPException(status_code=500, detail="创建用户失败")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建用户出错: {str(e)}")
    else:
        raise HTTPException(status_code=403, detail="没有权限执行此操作")
