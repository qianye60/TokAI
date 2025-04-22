# TokAI - 智能对话助手

TokAI 是一个现代化的全栈智能对话助手应用，提供流畅的对话体验和优雅的用户界面，支持多种AI模型接入。

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

## 安装与运行

```bash
# 切换到前端代码目录 (如果你的 package.json 在 Vue3 目录下)
cd Vue3

# 安装依赖
npm install

# 启动开发服务器 (通常带有热重载)
npm run dev

# 构建用于生产环境的应用
npm run build

# 预览生产构建的应用
npm run preview
```

## 贡献指南

我们欢迎各种形式的贡献，包括但不限于：提交 Bug 报告、提出功能建议、改进代码或文档。请通过提交 Issue 或 Pull Request 的方式参与。

## 许可证

本项目采用 [MIT License](LICENSE) 授权。
