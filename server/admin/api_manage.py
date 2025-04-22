from user.user import verify_token
from sqlite.db_api import get_api,create_api,delete_api,update_api,get_models,get_selectModel,update_api_model
from fastapi import Depends
from model.api_model import ApiKey, UpdateApiModel
from typing import List
from fastapi import APIRouter

api = APIRouter()

#添加API
@api.post('/api')
async def Add_api(api_data: ApiKey, token:dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        # 确保创建新API时不使用提供的ID
        # 兼容不同版本的SQLModel/Pydantic
        try:
            # 尝试使用新版方法
            api_data_dict = api_data.model_dump()
        except AttributeError:
            # 兼容旧版，使用dict()
            api_data_dict = dict(api_data)
            
        if "id" in api_data_dict:
            api_data_dict.pop("id")  # 移除id字段，让数据库自动生成

        new_api = ApiKey(**api_data_dict)
        result = await create_api(new_api)
        if result:
            return {"success": True}
        else:
            return {"error": "添加失败"}
    else:
        return {"error": "权限不足"}

#删除API
@api.delete('/api/{api_id}')
async def Delete_api(api_id: int, token:dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        result = await delete_api(api_id)
        if result:
            return {"success": True}
        else:
            return {"error": "删除失败"}
    else:
        return {"error": "权限不足"}

#获取API
@api.get('/api')
async def Get_api(token: dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        api_keys : List[ApiKey] = await get_api()
        return  {"api": [
            {
                "id": api_key.id,
                "api_name": api_key.api_name,
                "api_url": api_key.api_url,
                "api_key": api_key.api_key
            } for api_key in api_keys]}
    else:
        return {"error": "权限不足"}

#更新API
@api.put('/api')
async def Update_api(api_data: ApiKey, token:dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        # 确保ID存在且有效
        if not api_data.id:
            return {"error": "缺少API ID，无法更新"}

        # 检查API是否存在
        existing_apis = await get_api()
        api_exists = any(api.id == api_data.id for api in existing_apis)

        if not api_exists:
            return {"error": "API不存在，无法更新"}

        result = await update_api(api_data)
        if result:
            return {"success": True}
        else:
            return {"error": "更新失败"}
    else:
        return {"error": "权限不足"}


@api.get('/models/{api_id}')
async def Get_model(api_id: int, token:dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        models = await get_models(api_id)  # 移除 await，因为 get_models 现在是同步函数
        selectModels = await get_selectModel(api_id)
        if models and selectModels:
            return {"models": [{"model_id": model["id"], "model_owned_by": model["owned_by"]} for model in models],
                    "select": [model.model_name for model in selectModels]}
        elif models:
            return {"models": [{"model_id": model["id"], "model_owned_by": model["owned_by"]} for model in models],
                    "select": []}
        elif selectModels:
            return {"models": [], "select": [model.model_name for model in selectModels]}
        else:
            return {"models": [], "select": [],"error": "未找到模型"}
    else:
        return {"error": "权限不足"}

@api.put('/model')
async def Update_model(model_data: UpdateApiModel, token:dict = Depends(verify_token)):
    if token["userauth"] == 1 or token["userauth"] == 2:
        result = await update_api_model(model_data)
        if result:
            return {"success": True}
        else:
            return {"error": "更新失败"}
    else:
        return {"error": "权限不足"}
