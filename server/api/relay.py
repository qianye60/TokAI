from fastapi import APIRouter,Depends
from upfile.upfile import file_list
import os

from model.api_model import ApiKey
from model.chat_model import chat_model
from api.new_api import new_api_option, new_api
from user.user import verify_user
from sqlite.db_api import get_api, get_Models,get_selectModel
from sqlite.db_user import get_user
from typing import List
from fastapi.responses import StreamingResponse

# 将init定义为APIRouter对象，而不是函数
api = APIRouter()

@api.get('/models')
async def getModels():
    models = await get_Models()
    return {"models": models}

@api.post('/chat')
async def chat_handler(chat:chat_model,username:str=Depends(verify_user)):
    user = await get_user(username)

    if username != chat.username:
        return {"error": "用户不匹配！"}

    if user.money <= 0:
        return {"error": "余额不足"}
    api_keys:List[ApiKey] = await get_api()
    #测试是否有api_key和模型
    api = None
    #迭代查找令牌
    for api_key in api_keys:
        if not api_key:
            continue
        if api_key.api_name == chat.api_name:
            api = api_key
            models = await get_selectModel(api.id)
            for model in models:
                if chat.model_name in model.model_name:
                    file_urls = []
                    for file_id in chat.filelist_id:
                        if(file_id in chat.filelist_id):
                            # 构建文件的完整路径
                            file_path = os.path.join("temp", file_id)
                            # 检查文件是否存在
                            if os.path.exists(file_path):
                                # 可以选择返回相对路径或构建完整URL
                                file_urls.append(file_path)
                                file_list.remove(file_id)
                            else:
                                print(f"文件不存在: {file_path}")
                    if api.api_name == "newapi":
                        headers,json_data = await new_api_option(api, chat, file_urls)
                        
                        return StreamingResponse(new_api(username,headers,json_data,api), media_type="text/event-stream")
                    else:
                        return {"error": "API密钥未找到"}
    return {"error": "无此模型或API"}
                


                