

# TokAI - 智能对话助手

TokAI 是一个现代化的全栈智能对话助手应用，提供流畅的对话体验和优雅的用户界面，支持多种AI模型接入。

## 默认账号密码

- **admin**
- **123456**
### 登陆后记得修改账号密码
  
## 功能特点

-   🎨 **主题定制**
    -   **明暗模式切换**：支持浅色和深色两种视觉主题，满足不同环境下的使用偏好
    -   **实时应用**：主题更改即时生效，无需刷新
    -   **偏好记忆**：自动保存用户选择的主题设置

-   💬 **核心对话功能**
    -   **对话管理**：轻松创建新对话、重命名现有对话以及删除不需要的对话
    -   **批量操作**：提供批量删除对话的功能，方便管理
    -   **历史记录**：自动保存对话过程，方便回顾
    -   **多模型支持**：支持接入OpenAI、Google等多种AI服务

-   👤 **用户系统**
    -   **账户管理**：用户注册、登录和权限控制
    -   **邮箱验证**：支持邮箱验证功能
    -   **管理后台**：提供管理员控制面板

-   🎯 **用户界面与体验**
    -   **响应式设计**：侧边栏和整体布局能自适应不同屏幕尺寸
    -   **流畅动画**：界面交互包含优雅自然的过渡效果
    -   **现代化组件**：采用 Ant Design Vue 构建，提供高质量、一致性的 UI 元素
## 部署 (Deployment)

推荐使用 Docker Compose 进行部署，可以一键启动所有服务（前端、后端、Nginx）。

### 使用 Docker Compose (推荐)

1.  确保你的机器上安装了 Docker 和 Docker Compose。
2.  在项目根目录下，找到 `docker-compose.yml` 文件。
3.  根据需要修改 `.env` 文件（如果 `docker-compose.yml` 中使用了环境变量）或直接修改 `docker-compose.yml` 中的配置（例如端口映射）。
4.  在项目根目录下打开终端，运行以下命令：

    ```bash
    # 下载docker-compose.yaml，在所在目录下执行下面命令部署
    docker-compose up -d

    # 查看运行状态
    docker-compose ps

    # 查看日志
    docker-compose logs -f

    # 停止并移除容器、网络
    docker-compose down
    ```

### 使用 Docker 命令 (手动部署，更复杂)

使用单独的 `docker run` 命令部署多容器应用比较繁琐，你需要：

1.  **构建镜像**：分别为前端（通常是构建静态文件后用 Nginx 服务）和后端构建 Docker 镜像。
    ```bash
    # 构建后端镜像 (假设 Dockerfile 在 server/ 目录下)
    docker build -t tokai-backend:latest ./server

    # 构建前端镜像 (需要一个服务静态文件的 Dockerfile，例如使用 Nginx)
    # cd Vue3 && npm run build # 先构建前端静态文件
    # docker build -t tokai-frontend:latest . # 假设 Vue3 目录下有相应 Dockerfile
    ```
2.  **创建网络**：创建一个 Docker 网络，让容器可以互相通信。
    ```bash
    docker network create tokai-net
    ```
3.  **启动后端容器**：
    ```bash
    docker run -d --name tokai-backend-container --network tokai-net \
      -v ./data/sqlite:/app/sqlite \ # 示例：挂载数据库卷
      -p 8000:8000 \ # 示例：映射端口 (如果 Nginx 代理，此端口可能不需要暴露给主机)
      # -e ENV_VAR=value \ # 添加所需环境变量
      tokai-backend:latest
    ```
    *注意：* 这里的 `-v ./data/sqlite:/app/sqlite` 是一个示例，你需要根据实际情况调整数据库文件在容器内的路径和宿主机的挂载点。端口映射 `-p 8000:8000` 如果有 Nginx 作为反向代理，可能不需要直接暴露给宿主机，而是让 Nginx 容器访问。
4.  **启动前端/Nginx 容器**：你需要一个配置好的 Nginx 容器来服务前端静态文件，并将 API 请求代理到后端容器。
    ```bash
    docker run -d --name tokai-nginx-container --network tokai-net \
      -p 80:80 -p 443:443 \ # 映射 HTTP 和 HTTPS 端口
      -v ./nginx.conf:/etc/nginx/nginx.conf:ro \ # 挂载 Nginx 配置
      -v ./Vue3/dist:/usr/share/nginx/html:ro \ # 挂载前端构建产物
      # -v /path/to/ssl/certs:/etc/nginx/certs:ro \ # 如果使用 HTTPS，挂载证书
      nginx:latest # 或者你构建的包含前端文件的 Nginx 镜像 tokai-frontend:latest
    ```
    *注意：* Nginx 的配置 (`nginx.conf`) 需要正确设置 `server_name`、静态文件路径 (`root`) 以及反向代理 (`proxy_pass`) 到后端容器名 (`tokai-backend-container`) 和端口 (8000)。

**强烈建议**：对于这种多服务的应用，直接使用 `docker-compose` 会极大简化部署和管理过程。上面的 `docker run` 命令仅为示例，实际操作可能需要根据你的具体配置进行调整。

## 技术栈

### 前端
-   **框架**：Vue 3 + TypeScript
-   **状态管理**：Pinia
-   **UI组件库**：Ant Design Vue
-   **样式处理**：SCSS
-   **构建工具**：Vite
-   **Markdown渲染**：markdown-it, highlight.js

### 后端
-   **框架**：FastAPI (Python)
-   **数据库**：SQLite
-   **身份验证**：JWT
-   **API中继**：支持转发到OpenAI、Google等AI服务提供商
-   **服务器**：Uvicorn

### 部署
-   **容器化**：Docker
-   **编排**：Docker Compose
-   **Web服务器**：Nginx

## 项目结构

```
项目根目录/
├── Vue3/                # 前端应用
│   ├── public/          # 静态资源
│   ├── src/             # 源代码
│   │   ├── assets/      # 本地资源 (会被 Vite 处理)
│   │   ├── components/  # 可复用 UI 组件
│   │   ├── constants/   # 常量定义
│   │   ├── hooks/       # Composition API Hooks
│   │   ├── interface/   # TypeScript 类型定义
│   │   ├── layouts/     # 布局组件
│   │   ├── pages/       # 页面级组件
│   │   ├── router/      # 路由配置
│   │   ├── services/    # API 请求封装
│   │   ├── store/       # Pinia 状态管理
│   │   ├── styles/      # 全局样式与 SCSS 变量
│   │   ├── utils/       # 工具函数
│   │   ├── App.vue      # 根组件
│   │   └── main.ts      # 入口文件
│   ├── index.html       # 入口HTML文件
│   ├── package.json     # 前端依赖配置
│   └── vite.config.ts   # Vite配置文件
│
├── server/              # 后端应用
│   ├── admin/           # 管理员功能
│   │   ├── admin.py     # 管理接口路由
│   │   ├── api_manage.py # API密钥管理
│   │   ├── config_manage.py # 系统配置管理
│   │   ├── email_manage.py # 邮件设置管理
│   │   └── user_manage.py # 用户管理
│   ├── api/             # AI服务API
│   │   ├── google.py    # Google AI接口
│   │   ├── new_api.py   # 通用API接口
│   │   ├── openai.py    # OpenAI接口
│   │   └── relay.py     # API中继服务
│   ├── chat/            # 对话功能
│   │   ├── chat_manage.py # 对话管理
│   │   └── message_manage.py # 消息管理
│   ├── model/           # 数据模型
│   ├── sqlite/          # 数据库相关
│   ├── upfile/          # 文件上传
│   ├── user/            # 用户认证
│   ├── main.py          # 后端主入口
│   ├── requirements.txt # 后端依赖配置
│   └── Dockerfile       # 后端Docker配置
│
├── docker-compose.yml   # Docker编排配置
├── nginx.conf           # Nginx配置
├── LICENSE              # MIT许可证
└── README.md            # 项目说明文档
```

## 开发环境要求

-   Node.js >= 16
-   npm >= 7 (或 pnpm / yarn)
-   Docker & Docker Compose

## 本地开发运行

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd <project-root-directory>

# 2. 启动后端 (假设在项目根目录)
#    (根据你的后端设置，可能需要先创建虚拟环境并安装依赖)
#    pip install -r server/requirements.txt
#    uvicorn server.main:app --reload --port 8000 # 示例命令

# 3. 启动前端
cd Vue3

# 安装依赖
npm install

# 启动开发服务器 (通常带有热重载)
npm run dev

# 4. 构建用于生产环境的前端应用
# npm run build

# 5. 预览生产构建的应用
# npm run preview
```



## 贡献指南

我们欢迎各种形式的贡献，包括但不限于：提交 Bug 报告、提出功能建议、改进代码或文档。请通过提交 Issue 或 Pull Request 的方式参与。

## 许可证

本项目采用 [MIT License](LICENSE) 授权。
```
