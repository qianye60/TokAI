from sqlmodel import select
from .dbconfig import get_session
from model.user_model import Email
import traceback


# 数据库操作函数
async def get_email() -> Email | None:
    """获取邮箱配置"""
    try:
        session = next(get_session())
        
        result = session.exec(select(Email))
        email = result.first()
        
        if email:
            return email
        else:
            return None
    except Exception as e:
        print(f"获取邮箱配置出错: {str(e)}")
        traceback.print_exc()
        return None

async def update_email(email_config:Email) -> bool:
    try:
        session = next(get_session())
        
        result = session.exec(select(Email))
        email = result.first()
        
        if email:
            email.smtp_server = email_config.smtp_server
            email.sender = email_config.sender
            email.user = email_config.user
            email.port = email_config.port
            email.passwd = email_config.passwd
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"邮箱更新出错: {str(e)}")
        traceback.print_exc()
        return False