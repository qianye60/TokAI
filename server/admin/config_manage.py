from fastapi import APIRouter,Depends
from model.config_model import Config
from sqlite.db_config import get_config, update_config
from sqlite.dbconfig import get_session
from user.user import verify_token
from typing import Dict, Any

config = APIRouter()

@config.get("/config")
async def get_system_config():
    try:
        config = await get_config()
        if config is None:
            # 如果没有找到配置，返回默认值
            return Config()
        return config
    except Exception as e:
        print(f"配置错误: {str(e)}")
        # 出错时返回默认值
        return Config()
    
@config.put("/config")
async def update_system_config(config_data: Config, token = Depends(verify_token)):
    try:
        if token["userauth"] == 1 or token["userauth"] == 2:
            result = await update_config(config_data)
            if result:
                return await get_config()
            else:
                return {"error": "更新失败"}
        else:
            return {"error": "权限不足"}
    except Exception as e:
        print(f"配置错误: {str(e)}")   
        return {"error": str(e)}