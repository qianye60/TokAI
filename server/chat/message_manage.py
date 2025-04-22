from fastapi import APIRouter, Body,Depends,HTTPException
from model.chat_model import Create_message, Update_message, Delete_message
from sqlite.db_chat import create_message,update_message,delete_message
from user.user import verify_user,oauth2_scheme

message = APIRouter()

@message.post("/Createmessage")
async def createMessage(newmessage: Create_message ,username:str = Depends(verify_user)):
    try:
        if username != newmessage.username:
            raise HTTPException(status_code=403, detail="用户名不匹配")
        message_result = await create_message(newmessage)
        return {"message": "创建成功", "message_id": message_result.id}
    except Exception as e:
        return {"message": "创建失败", "detail": str(e)}

@message.post("/Updatemessage")
async def updatemessage(updatechat:Update_message,username:str = Depends(verify_user)):
    try:
        if username != updatechat.username:
            raise HTTPException(status_code=403, detail="用户名不匹配")
        await update_message(updatechat)
        return {"message": "更新成功"}
    except Exception as e:
        return {"message": "创建失败", "detail": str(e)}

@message.post("/Deletemessage")
async def deleteMessage(deletemessage:Delete_message,username:str = Depends(verify_user)):
    try:
        if username != deletemessage.username:
            raise HTTPException(status_code=403, detail="用户名不匹配")
        await delete_message(deletemessage)
        return {"message": "删除成功"}
    except Exception as e:
        return {"message": "删除失败", "detail": str(e)}
    