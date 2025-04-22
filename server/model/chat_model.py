from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
import uuid

# 导入循环引用的模型
if TYPE_CHECKING:
    from .user_model import User


class ChatConfig(BaseModel):
    message_max: int
    model_name: str
    api_name: str

class chatConfig(SQLModel, table=True):
    __tablename__ = "chatconfig"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    message_max: int
    model_name: str
    api_name: str
    username: str = Field(foreign_key="user.username")
    user: "User" = Relationship(back_populates="chatConfig")
    
    class Config:
        protected_namespaces = ()
    
# 历史消息APi
class HS_message(BaseModel):
    id: str
    isuser: bool
    content: str

class chat_model(BaseModel):
    username: str
    model_name: str  # 模型名称
    api_name: str    # API类型名称
    history_message: list[HS_message]
    message: str
    filelist_id: list[str]


#全部删除
class Delete_all(BaseModel):
    username: str
    
# 对话APi
# 创建
class Create_chat(BaseModel):
    username: str
    title: str

# 删除
class Delete_chat(BaseModel):
    username:str
    conversationId: str


# 更新
class Update_chat(BaseModel):
    username:str
    conversationId: str
    newtitle:str

# 消息API
#创建
class Create_message(BaseModel):
    username:str
    message:str
    isuser:bool
    conversationId:str

#删除
class Delete_message(BaseModel):
    username:str
    messageId:str

#更新
class Update_message(BaseModel):
    username:str
    message:str
    messageId:str


# SQLModel定义存储模型
class ChatDB(SQLModel, table=True):
    __tablename__ = "chat"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    createdAt: datetime

    username: str = Field(foreign_key="user.username")
    
    user: "User" = Relationship(back_populates="chats")
    messages: List["ChatMessageDB"] = Relationship(back_populates="chat")

class ChatMessageDB(SQLModel, table=True):
    __tablename__ = "chatmessages"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    isuser: bool
    content: str

    chat_id: Optional[str] = Field(default=None, foreign_key="chat.id")
    
    chat: Optional["ChatDB"] = Relationship(back_populates="messages")

# 已使用TYPE_CHECKING处理循环导入，不需要在底部直接导入
