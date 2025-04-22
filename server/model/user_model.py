from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Any, TYPE_CHECKING, Optional
from datetime import datetime

# 导入循环引用的模型
if TYPE_CHECKING:
    from .chat_model import ChatDB, chatConfig


class UserDB(BaseModel):
    username:str
    email:str
    hashed_password:str


class UserReg(BaseModel):
    username:str
    email:str
    code:str
    password:str

    
class User(SQLModel, table=True):
    __tablename__ = "user"  # 添加表名定义
    
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    money:float
    userauth:int
    
    # 关系定义
    chats: list["ChatDB"] = Relationship(back_populates="user")
    chatConfig: list["chatConfig"] = Relationship(back_populates="user")


class EmailRequest(BaseModel):
    email: EmailStr

class Email(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    smtp_server: str
    sender : str
    user : str
    port: int
    passwd: str

class EmailConfig(SQLModel):
    smtp_server: str
    sender : str
    user : str
    port: int

class TokenData(BaseModel):
    username: str | None = None

#创建令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str


# 新增前端响应模型
class ChatMessageResponse(BaseModel):
    id: str
    isuser: bool
    content: str

class ChatItemResponse(BaseModel):
    id: str
    username: str
    title: str
    createdAt: datetime
    chatmessages: List[ChatMessageResponse] = []

class Userinfo(BaseModel):
    id: int
    username: str
    email: str
    money: float
    userauth: int


class UserResponse(BaseModel):
    userinfo: Userinfo
    chats: List[ChatItemResponse] = []

class LoginResponse(BaseModel):
    token: Token
    user: UserResponse

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    money: Optional[float] = None
    userauth: Optional[int] = None

class UserUpdateRequest(BaseModel):
    username: str
    current_password: str = None
    new_password: str = None

class ApiResponse(BaseModel):
    code: int
    msg: str
    data: Any = None
