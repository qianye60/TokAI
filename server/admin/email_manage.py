from fastapi import APIRouter,Depends
from sqlite.db_email import get_email,update_email
from user.user import verify_token
from user.email_send import send_email
from typing import Annotated
from model.user_model import EmailConfig, Email, EmailRequest

email = APIRouter()

@email.get("/email", response_model=EmailConfig)
async def get_email_config(token: Annotated[dict, Depends(verify_token)]):
    try:
        if token["islogin"] == False:
            return {"error": "令牌错误"}
        elif token["userauth"] != 1 and token["userauth"] != 2:
            return {"error": "权限不足"}
        elif token["userauth"] == 1 or token["userauth"] == 2:
            email_config = await get_email()
            if email_config is None:
                # 如果没有找到配置，返回默认值
                return EmailConfig(smtp_server="", sender="", user="", port=465)
            return EmailConfig(smtp_server=email_config.smtp_server, sender=email_config.sender, user=email_config.user, port=email_config.port)
        else:
            return {"error": "未知错误"}
    except Exception as e:
        print(f"邮箱配置错误: {str(e)}")
        # 出错时返回默认值
        return EmailConfig(smtp_server="", sender="", user="", port=465)

@email.put("/email")
async def update_email_config(email_config: Email, token: Annotated[dict, Depends(verify_token)]):
    try:
        if token["islogin"] == False:
            return {"error": "令牌错误"}
        elif token["userauth"] != 1 and token["userauth"] != 2:
            return {"error": "权限不足"}
        elif token["userauth"] == 1 or token["userauth"] == 2:
            result = await update_email(email_config)
            if result:
                return {"success": True}
            else:
                return {"error": "更新失败"}
        else:
            return {"error": "未知错误"}
    except Exception as e:
        print(f"邮箱更新错误: {str(e)}")
        return {"error": "更新失败"}

@email.post("/email_test")
async def email_test(email: EmailRequest, token: Annotated[dict, Depends(verify_token)]):
    try:
        if token["islogin"] == False:
            return {"error": "令牌错误"}
        elif token["userauth"] != 1 and token["userauth"] != 2:
            return {"error": "权限不足"}
        elif token["userauth"] == 1 or token["userauth"] == 2:
            result = await send_email(EmailRequest(email=email.email))
            if result is True:
                return {"success": True, "message": "测试邮件发送成功"}
            else:
                # 如果不是True，则是一个带有错误信息的字典
                error_msg = result.get("error", "未知错误")
                return {"success": False, "error": f"测试邮件发送失败: {error_msg}"}
        else:
            return {"error": "未知错误"}
    except Exception as e:
        print(f"邮箱测试错误: {str(e)}")
        return {"success": False, "error": f"测试失败: {str(e)}"}