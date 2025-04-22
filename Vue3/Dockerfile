# Stage 1: Build the Vue application
FROM node:20-alpine as build-stage

WORKDIR /app

# 1. 复制依赖文件
COPY package*.json ./

# 2. 安装项目依赖（包含npm-run-all）
RUN npm install --unsafe-perm && \
    chmod -R 755 node_modules/.bin

# 3. 复制项目文件
COPY . .

# 4. 构建
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
