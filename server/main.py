#需求包或模块
import uvicorn
from fastapi.middleware.cors import CORSMiddleware #跨域访问请求配置
from fastapi import FastAPI #类型注解

#引入子级API
from user.user import user
from upfile.upfile import upfile
from sqlite.dbconfig import *
from user.email_send import email_router
from api.relay import api
from chat.chat_manage import chat
from chat.message_manage import message
from admin.admin import admin



app = FastAPI()#网站上线需要增加参数关闭测试文档 docs_url=None, redoc_url=None,openapi_url=None

# 在应用启动时初始化数据库
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user, prefix='/user',tags=['注册登录'])
app.include_router(upfile,prefix='/upfile',tags=['上传文件'])
app.include_router(sqlite,prefix='/sqlite',tags=['数据库'])
app.include_router(email_router,prefix='/email',tags=['邮箱'])
app.include_router(api,prefix='/api',tags=['中继'])
app.include_router(chat,prefix='/chat',tags=['对话存储和同步'])
app.include_router(message,prefix='/message',tags=['消息存储和同步'])
app.include_router(admin,prefix='/admin',tags=['管理'])


# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 允许的源
    allow_credentials=True,  # 如果需要支持 cookies，设置为 True
    allow_methods=["*"],      # 允许所有方法 ("GET", "POST", "PUT", etc.)
    allow_headers=["*"],      # 允许所有头
)

@app.get("/")
async def root():
    return "Hello!"

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=40000)
    

