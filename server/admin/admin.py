from fastapi import APIRouter
from admin.email_manage import email
from admin.user_manage import user
from admin.config_manage import config
from admin.api_manage import api


admin = APIRouter()

admin.include_router(email, prefix="", tags=["邮箱"])
admin.include_router(user, prefix="", tags=["用户管理"])
admin.include_router(config, prefix="", tags=["配置管理"])
admin.include_router(api, prefix="", tags=["API管理"])