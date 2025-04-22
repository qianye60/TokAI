from ast import List
from model.api_model import ApiKey, ApiModel, UpdateApiModel
from model.chat_model import ChatConfig, chatConfig
from sqlite.dbconfig import get_session, select
import httpx


async def get_api() -> ApiKey | None:
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey)).all()
        return result
    except Exception as e:
        print(f"获取API密钥失败: {str(e)}")
        return None

async def create_api(Api: ApiKey) -> bool:
    try:
        Session = next(get_session())
        new_api = ApiKey(
            api_name=Api.api_name,
            api_url=Api.api_url,
            api_key=Api.api_key
        )
        Session.add(new_api)
        Session.commit()
        return True
    except Exception as e:
        print(f"创建API密钥失败: {str(e)}")
        return False

async def update_api(Api: ApiKey) -> bool:
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey).where(ApiKey.id == Api.id)).one_or_none()
        if result:
            result.api_key = Api.api_key
            result.api_name = Api.api_name
            result.api_url = Api.api_url
            Session.commit()
            return True
    except Exception as e:
        print(f"更新API密钥失败: {str(e)}")
        return False

async def delete_api(api_id: int) -> bool:
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey).where(ApiKey.id == api_id)).one_or_none()
        if result:
            Session.delete(result)
            Session.commit()
            return True
    except Exception as e:
        print(f"删除API密钥失败: {str(e)}")
        return False

async def get_models(api_id: int):
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey).where(ApiKey.id == api_id)).first()
        baseurl = result.api_url[:result.api_url.find("/v1")]
        response = httpx.get(f"{baseurl}/v1/models", headers={"Authorization": f"Bearer {result.api_key}"})
        result = response.json()
        if result.get("success",False):
            models = result.get("data", [])
            return models
        else:
            return False
    except Exception as e:
        print(f"获取所有模型失败: {str(e)}")
        return None
    except Exception as e:
        print(f"获取所有失败: {str(e)}")
        return None

async def get_selectModel(api_id: int):
    #获取api对应模型
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey).where(ApiKey.id == api_id)).first()
        Session.refresh(result)
        return result.api_model
    except Exception as e:
        print(f"获取选中模型失败: {str(e)}")
        return None

async def update_api_model(model_data: UpdateApiModel) -> bool:
    #更新api对应模型
    try:
        Session = next(get_session())
        result = Session.exec(select(ApiKey).where(ApiKey.id == model_data.api_id)).first()
        if result:
            Session.refresh(result)

            # 先删除现有的所有模型关联
            # 查询当前与该API关联的所有模型
            existing_models = Session.exec(select(ApiModel).where(ApiModel.api_key_id == model_data.api_id)).all()
            # 删除这些模型
            for model in existing_models:
                Session.delete(model)

            # 创建新的模型关联
            for model_name in model_data.models:
                new_model = ApiModel(model_name=model_name, api_key_id=model_data.api_id)
                Session.add(new_model)

            Session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"更新API模型失败: {str(e)}")
        return False

async def get_Models() -> List:
    #获取所有模型-前端用户使用，只返回名字
    try:
        Session = next(get_session())
        data = []
        result = Session.exec(select(ApiKey)).all()
        for api in result:
            Session.refresh(api)
            data.append({
                "model_owned_by": api.api_name,
                "model_id": [model.model_name for model in api.api_model]
            })
        return data
    except Exception as e:
        print(f"获取选中模型失败: {str(e)}")
        return None

async def get_chat_config(username: str) -> ChatConfig:
    try:
        Session = next(get_session())
        result = Session.exec(select(chatConfig).where(chatConfig.username == username)).first()
        if not result:
            # 如果没有找到记录，创建一个新的 ChatConfig 并提供默认值
            return ChatConfig(message_max=8, model_name="gpt-3.5-turbo", api_name="newapi")
        # 如果找到了，将 SQLModel 实例转换为 BaseModel 实例
        return ChatConfig(message_max=result.message_max, model_name=result.model_name, api_name=result.api_name)
    except Exception as e:
        print(f"获取配置失败: {str(e)}")
        # 出错时返回默认配置
        return ChatConfig(message_max=8, model_name="gpt-3.5-turbo", api_name="newapi")

async def update_chat_config(config: ChatConfig,username:str) -> bool:
    try:
        Session = next(get_session())
        result = Session.exec(select(chatConfig).where(chatConfig.username == username)).first()
        if result:
            Session.refresh(result)
            result.message_max = config.message_max
            result.model_name = config.model_name
            result.api_name = config.api_name
            Session.commit()
            return True
        else:
            Session.add(chatConfig(username=username, message_max=config.message_max, model_name=config.model_name, api_name=config.api_name))
            Session.commit()
            return True
    except Exception as e:
        print(f"更新配置失败: {str(e)}")
        return False
