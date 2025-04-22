import httpx
import json
import base64
from typing import List
from model.api_model import ApiKey
from model.chat_model import chat_model
from model.user_model import User
from sqlite.db_config import get_session
from sqlmodel import select

async def new_api(username,headers, json_data, api: ApiKey):
    timeout = httpx.Timeout(60.0)
    content_text = ''

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            try:
                # 使用显式的Session并检查查询结果
                session = next(get_session())

                user = session.exec(select(User).where(User.username == username)).first()

            except Exception as e:
                print(f"访问用户属性失败: {str(e)}")
            async with client.stream('POST', api.api_url,
                                    headers=headers, json=json_data) as response:
                async for line in response.aiter_lines():
                    if not line or not line.startswith('data: '):
                        continue

                    if line == 'data: [DONE]':
                        # 计算token
                        try:
                            # 计算提示词token
                            prompt_text = ""
                            # 处理所有消息，不只是第一条
                            for message in json_data['messages']:
                                # 处理多模态内容
                                if isinstance(message.get('content'), list):
                                    for item in message['content']:
                                        if item.get('type') == 'text':
                                            prompt_text += item.get('text', '')
                                else:
                                    # 处理纯文本内容
                                    prompt_text += str(message.get('content', ''))

                            # token估算 - 中文约1字1token，英文约4字符1token
                            def estimate_tokens(text):
                                chinese_char_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                                other_char_count = len(text) - chinese_char_count
                                return (
                                    chinese_char_count +  # 中文字符数量
                                    (other_char_count // 4) +  # 英文字符数量整除4
                                    (1 if other_char_count % 4 else 0)  # 英文字符余数(有则加1)
                                )

                            # 计算token数量
                            prompt_tokens = max(1, estimate_tokens(prompt_text))
                            completion_tokens = max(1, estimate_tokens(content_text))
                            total_tokens = prompt_tokens + completion_tokens

                            # 计算扣除的金额 (使用更合理的比例，1000 tokens 花费 0.01 单位)
                            cost = total_tokens / 100000
                            original_money = float(user.money)
                            # 安全地访问money属性
                            try:
                                new_money = round(original_money - cost, 4)  # 保留4位小数
                                user.money = new_money
                                session.add(user)
                                session.commit()

                            except Exception as money_ex:
                                print(f"余额更新错误: {str(money_ex)}")

                            # 直接返回JSON
                            response_json = {"usage": {
                                "prompt_tokens": prompt_tokens,
                                "completion_tokens": completion_tokens,
                                "total_tokens": total_tokens
                            }, "finished": True}
                            yield json.dumps(response_json).encode() + b'\n'
                        except Exception as ex:
                            print(f"Token计算错误: {str(ex)}")
                            # 记录更详细的错误信息，帮助调试
                            import traceback
                            print(f"错误详情: {traceback.format_exc()}")

                            # 安全回退：确保至少扣除最小费用
                            try:
                                user.money = user.money - 0.001
                                session.add(user)
                                session.commit()
                            except Exception as money_ex:
                                print(f"最小扣款失败: {str(money_ex)}")

                            yield b'{"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2},"finished":true}\n'
                        break

                    try:
                        data = json.loads(line[6:])
                        content = data["choices"][0]["delta"].get("content", "")
                        if content:
                            content_text += content
                            # 直接返回JSON
                            response_json = {"content": content}
                            yield json.dumps(response_json).encode() + b'\n'
                    except Exception as e:
                        # 直接返回JSON
                        error_msg = str(e)
                        print(f"请求错误: {error_msg}")
                        response_json = {"error": error_msg, "finished": True}
                        yield json.dumps(response_json).encode() + b'\n'
        except Exception as e:
            error_str = str(e)
            print(f"请求错误: {error_str}")
            response_json = {"error": error_str, "finished": True}
            yield json.dumps(response_json).encode() + b'\n'

async def new_api_option(api:ApiKey,chat:chat_model,file_urls:List[str]):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api.api_key,
    }
    #对话记录
    messages = []

    for hsmessage in chat.history_message:
        messages.append({
            'role': 'user' if hsmessage.isuser else 'assistant',
            'content': hsmessage.content  # 直接使用内容文本，不要包装成对象
        })

    content_list = [{"type": "text", "text": chat.message}]

    # 修改图片URL构建方式
    for file_path in file_urls:
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            content_list.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            })

    # 将历史消息和当前消息合并
    messages.append({
        'role': 'user',
        'content': content_list
    })

    json_data = {
        'model': chat.model_name,
        'messages': messages,
        'stream': True,
    }
    return headers,json_data
