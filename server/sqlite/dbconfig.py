from sqlmodel import Session, create_engine, select, SQLModel
from fastapi import APIRouter
# 从各个独立模型文件导入所需模型
from model.user_model import User, Email
from model.chat_model import ChatDB, ChatMessageDB, chatConfig
from model.api_model import ApiKey
from model.config_model import Config
from tools.token import get_password_hash

sqlite = APIRouter()

#数据库配置
import os

sqlite_file_name = "TokAI.db"
# 使用绝对路径确保数据库文件位置正确
server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(server_dir, "data")
os.makedirs(data_dir, exist_ok=True)  # 确保 data 目录存在

sqlite_url = f"sqlite:///{os.path.join(data_dir, sqlite_file_name)}"
#创建数据库
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

#创建数据库会话
def get_session():#生成器创建数据库会话
    with Session(engine) as session:
        yield session

def init():
    Session = next(get_session())
    users = Session.exec(select(User)).all()
    #初始化用户
    if not users:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("123456"),
            money=1000.0,
            userauth=2  # 2是超级管理员权限
        )
        Session.add(admin)
        Session.commit()
        print("已创建管理员账户")
    #初始化系统配置
    config = Session.exec(select(Config)).all()
    if not config:
        config_init = Config(email_register=False,title="TokAI",guest=False,default_money=0)
        Session.add(config_init)
        Session.commit()
        print("已初始化系统配置")
    #初始化邮箱配置
    email = Session.exec(select(Email)).all()
    if not email:
        email_init = Email(smtp_server="", sender="", user="", port=465, passwd="")
        Session.add(email_init)
        Session.commit()
        print("已初始化邮箱配置")
    
#创建启动表
def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)
    # 初始化数据
    init()
