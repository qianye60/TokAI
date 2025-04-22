from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

# 导入循环引用的模型
if TYPE_CHECKING:
    from .chat_model import ChatDB

class ApiKey(SQLModel, table=True):
    __tablename__ = "apikey"
    

    id: int = Field(default=None, primary_key=True)
    api_key: str
    api_name: str
    api_url: str

    # 关系定义 - 一对多
    api_model: List["ApiModel"] = Relationship(back_populates="api_key")


class ApiModel(SQLModel, table=True):
    __tablename__ = "apimodel"
    
    id: int = Field(default=None, primary_key=True)
    model_name: str

    # 外键定义
    api_key_id: Optional[int] = Field(default=None, foreign_key="apikey.id")

    # 关系定义 - 多对一
    api_key: Optional["ApiKey"] = Relationship(back_populates="api_model")

    class Config:
        protected_namespaces = ()

class UpdateApiModel(BaseModel):
    api_id: int
    models: List[str]
