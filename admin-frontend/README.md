# 消息通知平台 - 管理后台

基于 Vue 3 + TypeScript + Element Plus 的现代化管理后台。

## 技术栈

- **框架**: Vue 3.4+
- **构建工具**: Vite 5.0+
- **UI组件库**: Element Plus 2.4+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **图表库**: ECharts 5.4+
- **开发语言**: TypeScript 5.3+

## 功能特性

### ✅ 已实现功能

- 🔐 **登录认证** - 基于JWT Token的认证机制
- 📊 **Dashboard** - 系统概览、数据统计、趋势图表
- 💌 **消息管理** - 消息列表、详情查看、状态筛选
- 📝 **模板管理** - 模板列表、版本管理
- 📧 **邮箱管理** - 邮箱配置、连接测试、状态监控

### 🎨 UI特性

- 🎯 现代化设计风格
- 📱 响应式布局
- 🌈 丰富的交互体验
- 💨 流畅的页面切换动画
- 🎭 Element Plus完整图标库

## 项目结构

```
admin-frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   ├── auth.ts        # 认证API
│   │   ├── message.ts     # 消息API
│   │   ├── template.ts    # 模板API
│   │   ├── emailAccount.ts # 邮箱API
│   │   └── monitoring.ts  # 监控API
│   ├── assets/            # 资源文件
│   ├── components/        # 公共组件
│   ├── router/            # 路由配置
│   │   └── index.ts
│   ├── stores/            # 状态管理
│   │   ├── user.ts        # 用户状态
│   │   └── app.ts         # 应用状态
│   ├── styles/            # 全局样式
│   │   └── index.css
│   ├── utils/             # 工具函数
│   │   └── request.ts     # Axios封装
│   ├── views/             # 页面组件
│   │   ├── Layout.vue     # 主布局
│   │   ├── Login.vue      # 登录页
│   │   ├── Dashboard.vue  # 首页
│   │   ├── Messages/      # 消息管理
│   │   │   ├── Index.vue
│   │   │   └── Detail.vue
│   │   ├── Templates/     # 模板管理
│   │   │   └── Index.vue
│   │   └── EmailAccounts/ # 邮箱管理
│   │       └── Index.vue
│   ├── App.vue            # 根组件
│   └── main.ts            # 入口文件
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 快速开始

### 安装依赖

```bash
# 进入项目目录
cd admin-frontend

# 安装依赖（推荐使用pnpm）
pnpm install

# 或使用npm
npm install

# 或使用yarn
yarn install
```

### 开发模式

```bash
# 启动开发服务器
npm run dev

# 访问地址: http://localhost:8080
```

### 生产构建

```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 环境配置

### 开发环境 (.env.development)

```env
VITE_APP_TITLE=消息通知平台管理后台
VITE_API_BASE_URL=/api
VITE_APP_ENV=development
```

### 生产环境 (.env.production)

```env
VITE_APP_TITLE=消息通知平台管理后台
VITE_API_BASE_URL=/api
VITE_APP_ENV=production
```

## 登录凭证

### 默认API凭证

```
API Key: noti_aL3rBP1SGm8yy4havWd0xK-nAZlBq5kgrIoI7SmOhy8
API Secret: secret_5vEh7qvot63UhMQ_qomUM8BfToW-hJ_q
```

> 注意：生产环境请修改默认凭证！

## 代理配置

开发环境下，Vite自动代理API请求到后端：

```typescript
// vite.config.ts
server: {
  port: 8080,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // 后端API地址
      changeOrigin: true,
    },
  },
}
```

## 核心功能说明

### 1. Dashboard 首页

- 📊 实时数据统计（总消息数、成功数、失败数、成功率）
- 📈 24小时发送趋势图表（基于ECharts）
- 🔗 快捷操作入口
- ℹ️ 系统信息展示

### 2. 消息管理

- 📋 消息列表（支持分页）
- 🔍 状态筛选（待发送、发送中、成功、失败、重试中）
- 📝 详情查看（完整信息、HTML内容预览）
- 🕐 时间格式化显示

### 3. 模板管理

- 📄 模板列表展示
- 🏷️ 模板类型标签
- 📌 版本号显示
- ⚡ 启用/禁用状态

### 4. 邮箱管理

- 📧 邮箱账户列表
- 📊 发送进度条（今日发送/每日限额）
- 🧪 连接测试功能
- 🎯 优先级排序
- ✅ 状态监控（正常/不可用/禁用）

## API集成

所有API接口已完整集成，支持：

- ✅ 统一的响应格式处理
- ✅ 错误拦截和提示
- ✅ Token自动携带
- ✅ 401自动跳转登录
- ✅ 请求/响应拦截器
- ✅ TypeScript类型定义

## 路由守卫

- 🔐 自动检测登录状态
- 🚪 未登录自动跳转登录页
- 📄 动态页面标题
- 🎯 路由元信息支持

## 状态管理

### User Store (用户状态)

- Token管理
- 用户信息存储
- 登出功能
- localStorage持久化

### App Store (应用状态)

- 侧边栏折叠状态
- 全局配置管理

## 开发建议

### 添加新页面

1. 在 `src/views/` 下创建页面组件
2. 在 `src/router/index.ts` 中添加路由配置
3. 如需API，在 `src/api/` 下创建API文件

### 添加新API

```typescript
// src/api/xxx.ts
import { get, post } from '@/utils/request'

export function getXxx(params: any) {
  return get<ResponseType>('/v1/xxx', { params })
}
```

### 添加新Store

```typescript
// src/stores/xxx.ts
import { defineStore } from 'pinia'

export const useXxxStore = defineStore('xxx', () => {
  // 状态和方法
  return { ... }
})
```

## 部署

### Docker部署

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

### Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Edge >= 90
- Safari >= 14

## 常见问题

### Q: 登录后API请求401？

A: 检查Token是否正确保存，查看浏览器控制台网络请求的Authorization头。

### Q: 图表不显示？

A: 确保ECharts正确初始化，检查DOM元素是否存在。

### Q: 代理不工作？

A: 检查vite.config.ts中的proxy配置，确保后端服务已启动。

## 待完善功能

- [ ] 模板编辑功能
- [ ] 邮箱创建/编辑表单
- [ ] 统计分析页面
- [ ] 批量操作
- [ ] 导出功能
- [ ] 更多筛选选项
- [ ] 消息重发功能
- [ ] 实时通知（WebSocket）

## 许可证

MIT

---

**项目创建时间**: 2025-10-25  
**版本**: 1.0.0  
**作者**: AI Assistant

