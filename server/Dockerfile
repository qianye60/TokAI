FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 确保temp目录存在（用于文件上传）
RUN mkdir -p temp

# 暴露端口
EXPOSE 40000

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40000"]
