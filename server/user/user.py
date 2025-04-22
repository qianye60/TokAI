#三方库
from fastapi.security import OAuth2PasswordRequestForm
from .email_send import verify_code
from fastapi import APIRouter,Depends,HTTPException,status
from datetime import datetime, timedelta
from typing import Annotated
#调用自己模块
from sqlite.db_user import get_user,create_user,update_user_by_id
from model.user_model import User, Token, UserReg, UserDB, LoginResponse, UserResponse, ChatItemResponse, ChatMessageResponse, Userinfo, UserUpdateRequest, ApiResponse, UpdateUser
from tools.token import authenticate_user,ACCESS_TOKEN_EXPIRE_DAYS,create_access_token,get_password_hash,oauth2_scheme,SECRET_KEY,ALGORITHM
from jwt.exceptions import InvalidTokenError
import jwt
from sqlite.db_config import get_config
from uuid import uuid4

user = APIRouter()


#验证token
async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        
        # 获取用户，并处理用户不存在的情况
        user = await get_user(username)
        if user is None:
            print(f"用户不存在: {username}")
            return False
            
        return {"islogin": True, "userauth": user.userauth}
    except InvalidTokenError as e:
        print(f"Token验证失败: {str(e)}")
        return False
    except Exception as e:
        print(f"获取用户出错: {str(e)}")
        return False

    
#作为依赖项验证用户登录并且是自己的
async def verify_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if (await verify_token(token)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    else:
        raise HTTPException(status_code=401,detail="invalid token!")

#用户登录获取令牌
@user.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> LoginResponse:
    user_db : User = await get_user(form_data.username)
    if user_db is None:
        # 用户不存在则返回 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user = authenticate_user(user_db, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data = {"sub":user.username},
        token_expire = access_token_expires
    )
    
    # 使用模型构造返回数据
    token_response = Token(access_token=access_token, token_type="bearer")
    
    # 构造聊天消息列表
    chat_items = []
    for chat in user.chats:
        messages = []
        for msg in chat.messages:
            messages.append(ChatMessageResponse(
                id=msg.id,
                isuser=msg.isuser,
                content=msg.content
            ))
        
        chat_items.append(ChatItemResponse(
            id=chat.id,
            username=user.username,
            title=chat.title,
            createdAt=chat.createdAt,
            chatmessages=messages
        ))
    
    # 构造用户响应
    user_response = UserResponse(
        userinfo = Userinfo(
            id=user.id,
            username=user.username,
            email=user.email,
            money=user.money,
            userauth=user.userauth
        ),
        chats=chat_items
    )
    
    # 构造最终响应
    response = LoginResponse(token=token_response, user=user_response)
    
    return response

@user.post("/verify")
async def read_users_me(
    current_user: Annotated[dict, Depends(verify_token)],
):
    return current_user


#——————————————————————————————————————————注册—————————————————————————————————————————————————
@user.get('/info')
async def get_user_info(username:str = Depends(verify_user)):
    user = await get_user(username)
    return Userinfo(id=user.id, username=user.username, email=user.email, money=user.money, userauth=user.userauth)
    
@user.post("/register")
async def register(user:UserReg):
    try:
        config = await get_config()
        if config.email_register == True:
            code = verify_code.get(user.email,None)
            if code !=None:
                if code[1] < datetime.now():
                    return {'error':3} #验证码超时
                else:
                    if user.code == verify_code.get(f'{user.email}',False)[0]:
                        state = await create_user(UserDB(username=user.username,
                                                email=user.email,
                                                hashed_password=get_password_hash(user.password),
                                                ))
                        if state == '1':
                            return {'error':1}
                        elif state == '2':
                            return {'error':2}
                        return True
                    else:
                        return {'error':4}
            else:
                return {'error':4}
        elif config.email_register == False:
            state = await create_user(UserDB(username=user.username,
                                                email=str(uuid4()),
                                                hashed_password=get_password_hash(user.password),
                                                ))
            if state == '1':
                return {'error':1}
            elif state == '2':
                return {'error':2}
            return True
        else:
            return {'error':4}
    except Exception as e:
        return {"error": e}

#——————————————————————————————————————————用户信息更新—————————————————————————————————————————————————

@user.post("/update")
async def update_user_info(
    update_data: UserUpdateRequest,
    current_username: Annotated[str, Depends(verify_user)]
):
    try:
        # 获取当前用户信息
        user_db = await get_user(current_username)
        if not user_db:
            return ApiResponse(code=1, msg="用户不存在")
        
        # 创建要更新的数据对象
        update_user = UpdateUser(
            username=update_data.username,
            email=user_db.email,  # 保持原邮箱不变
            password=update_data.new_password if update_data.new_password else None,
            money=user_db.money,  # 保持原余额不变
            userauth=user_db.userauth  # 保持原权限不变
        )
        
        # 如果需要更改密码，验证当前密码
        if update_data.current_password and update_data.new_password:
            # 验证当前密码
            if not authenticate_user(user_db, update_data.current_password):
                return ApiResponse(code=2, msg="当前密码错误")
        
        # 更新用户信息
        updated_user = await update_user_by_id(user_db.id, update_user)
        if not updated_user:
            return ApiResponse(code=3, msg="更新失败")
            
        return ApiResponse(code=0, msg="更新成功", data={"username": updated_user.username})
    except HTTPException as e:
        return ApiResponse(code=e.status_code, msg=e.detail)
    except Exception as e:
        return ApiResponse(code=500, msg=f"服务器错误: {str(e)}")
