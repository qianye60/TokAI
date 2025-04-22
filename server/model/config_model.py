from sqlmodel import SQLModel, Field

class Config(SQLModel,table=True):
    __tablename__ = "config"
    id: int = Field(default=None, primary_key=True)
    title: str
    default_money: float
    email_register: bool
    guest: bool

    
    