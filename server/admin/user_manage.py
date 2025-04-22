from fastapi import APIRouter, Depends, HTTPException, status
from tools.token import oauth2_scheme
from sqlite.db_user import get_users,update_user_by_id,get_user_by_id,delete_user_by_id
from user.user import verify_token
from typing import Annotated, List
from model.user_model import User, Userinfo, UpdateUser

user = APIRouter()

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