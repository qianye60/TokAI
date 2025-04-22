from fastapi import APIRouter
from fastapi import UploadFile
from typing import List
from random import randint
import os
from uuid import uuid4
upfile = APIRouter()

file_list:list[str] = []

@upfile.post("/chatfile") #上传聊天框文件
async def chatfile(files: List[UploadFile]):
    # Read file content
    if (not(os.path.exists("temp"))):
        os.mkdir("temp")
    
    # MIME类型到文件扩展名的映射
    mime_to_extension = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'application/pdf': '.pdf',
        'text/plain': '.txt',
        'text/csv': '.csv',
        'application/json': '.json',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-excel': '.xls'
    }
    
    for file in files:
        # 从MIME类型获取文件扩展名
        file_extension = mime_to_extension.get(file.content_type, '.bin')  # 默认为.bin
        
        # 生成唯一文件名
        file_name = uuid4().hex + file_extension
        
        content = await file.read()
        # Save to file
        with open("temp/" + file_name, "wb") as f:
            f.write(content)
        file_list.append(file_name)
        print(file_list)
        return {"id": file_name}