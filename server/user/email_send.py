#调用三方库
from fastapi import APIRouter
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel,EmailStr
from random import randint
import base64
from datetime import datetime, timedelta

#调用自己模块
from sqlite.db_email import get_email,Email
from model.user_model import EmailRequest

email_router = APIRouter()


verify_code:dict[str:tuple[str,datetime]] = {}


@email_router.post('/send_email')
async def send_email(request: EmailRequest):
    code = verify_code.get(request.email,None)
    if code !=None:
        if code[1] > datetime.now():
            print({'error':"请求频繁！"})
            return {'error':"请求频繁！"}
    code_time = datetime.now() + timedelta(minutes=1)

    email:Email = await get_email()
    # 调试信息
    print(f"获取的邮箱配置: {email}")
    if email == None:
        return {'error':"邮箱未配置！"}
    # 更多调试信息
    print(f"发件人: {email.sender}, 用户: {email.user}, 端口: {email.port}")
    
    code = randint(100000,999999)
    receiver = request.email
    verify_code[receiver] = (str(code),code_time)
    
    # 使用HTML格式
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .code {{
                font-size: 24px;
                font-weight: bold;
                color: #1890ff;
                letter-spacing: 5px;
                text-align: center;
                margin: 20px 0;
                padding: 10px;
                background-color: #e6f7ff;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #999;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>验证码通知</h2>
            <p>尊敬的用户：</p>
            <p>您的验证码是：</p>
            <div class="code"><b>{code}</b></div>
            <p>此验证码用于账号注册，请勿泄露给他人。</p>
            <p>如非本人操作，请忽略此邮件。</p>
            <div class="footer">
                <p>此邮件由系统自动发送，请勿回复</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEText(html_content, 'html', 'utf-8')

    try:
        # 严格按照RFC标准设置From头
        msg['From'] = f'=?UTF-8?B?{base64.b64encode("系统通知".encode()).decode()}?= <{email.sender}>'
        msg['To'] = receiver
        msg['Subject'] = f'=?UTF-8?B?{base64.b64encode("验证码".encode()).decode()}?='

        smtp = smtplib.SMTP_SSL(email.smtp_server, email.port)
        smtp.login(email.user, email.passwd)
        smtp.sendmail(email.sender, receiver, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(f"邮件发送错误: {str(e)}")
        return {"error": str(e)}

