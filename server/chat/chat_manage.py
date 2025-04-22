from fastapi import APIRouter, Body,Depends,HTTPException
from model.chat_model import Create_chat, Delete_chat, Update_chat, Delete_all, ChatConfig
from sqlite.db_chat import create_chat, delete_chat, update_chat, delete_all
from user.user import verify_user, oauth2_scheme
from sqlite.db_api import update_chat_config, get_chat_config

chat = APIRouter()

@chat.post("/Deleteall")
async def deleteAll(deleteall:Delete_all,username:str=Depends(verify_user)):
    try:
        if(username == deleteall.username):
            chat_result = await delete_all(deleteall)
            return {"message": "删除成功"}
    except Exception as e:
        return {"message": "删除失败"}
        

@chat.post("/Createchat")
async def createChat(newchat: Create_chat ,username:str = Depends(verify_user)):
    try:
        if(username == newchat.username):
            chat_result = await create_chat(newchat)
            return {"message": "创建成功", "chat_id": chat_result.id}
    except Exception as e:
        return {"message": "创建失败", "detail": str(e)}

@chat.post("/Deletechat")
async def deleteChat(deletechat: Delete_chat, username: str = Depends(verify_user)):
    try:
        if(username == deletechat.username):
            chat_result = await delete_chat(deletechat)
            return {"message": "删除成功"}
    except Exception as e:
        return {"message": "删除失败", "detail": str(e)}
    
@chat.post("/Updatechat")
async def updateChat(updatechat:Update_chat,username:str = Depends(verify_user)):
    try:
        if(username == updatechat.username):
            chat_result = await update_chat(updatechat)
            return {"message": "更新成功"}
    except Exception as e:
        return {"message": "更新失败", "detail": str(e)}


@chat.post('/config')
async def getApi(config:ChatConfig, username:str=Depends(verify_user)):
    if config.message_max < 1:
        return {"message": "对话历史限制必须大于0"}
    if config.message_max > 20:
        return {"message": "对话历史限制必须小于等于20"}
    if config.model_name == "":
        return {"message": "请选择模型"}
    return await update_chat_config(config, username)

@chat.get('/config')
async def getApi(username:str=Depends(verify_user)):
    return await get_chat_config(username)
