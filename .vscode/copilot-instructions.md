# Copilot Instructions for give_me_ssl Project

## 项目概述
**项目中文名**: SSL证书管理平台  
**项目英文名**: give me ssl  

这是一个免费SSL证书管理系统，提供从申请到部署的一站式SSL证书管理服务。用户可以通过系统：
- 获取免费SSL证书 (Let's Encrypt、阿里云)
- 选择证书格式 (nginx、apache、tomcat等)
- 自动/手动部署证书到目标服务器
- 监控证书状态和到期提醒
- 支持多种登录方式和通知渠道

**技术架构**: 前后端分离
- 后端：Django 5.2.6 + DRF + Python 3.12
- 前端：Vue 3 + TypeScript + Vite 7
- 数据库：SQLite3 (开发) / PostgreSQL (生产)
- 认证：JWT Token

## 项目结构
```
give_me_ssl/
├── server/              # Django 后端
│   ├── manage.py
│   ├── server/         # Django 配置
│   ├── apps/           # 业务应用
│   │   ├── accounts/   # 用户认证
│   │   ├── certificates/ # 证书管理
│   │   ├── providers/  # CA提供商
│   │   ├── notifications/ # 通知系统
│   │   └── settings/   # 系统设置
│   └── .venv/          # Python 虚拟环境
└── web/                # Vue 前端
    ├── src/
    │   ├── components/ # 公共组件
    │   ├── views/      # 页面视图
    │   ├── stores/     # Pinia 状态管理
    │   ├── router/     # 路由配置
    │   ├── locales/    # 国际化文件
    │   └── utils/      # 工具函数
    ├── .env.development    # 开发环境配置
    ├── .env.test          # 测试环境配置
    ├── .env.staging       # 预发布环境配置
    └── .env.production    # 生产环境配置
```

## 编码规范

### 后端 (Django/Python 3.12)
- 使用 Django 5.2+ 最新特性
- 遵循 PEP 8 代码规范
- 使用类型注解 (Type Hints)
- API 设计遵循 RESTful 原则
- 使用 Django ORM 进行数据库操作
- 敏感信息加盐存储到数据库
- 错误处理使用 Django 异常类
- 所有Python命令前需激活虚拟环境: `source server/.venv/bin/activate`

### 前端 (Vue 3 + TypeScript)
- 使用 Vue 3 Composition API (setup语法糖)
- 严格使用 TypeScript，避免 any 类型
- 组件使用 PascalCase 命名，文件名使用 kebab-case
- 使用 Pinia 进行状态管理
- 路由懒加载优化性能
- 支持国际化 i18n，自动识别浏览器语言
- 使用 Element Plus UI 组件库
- 丰富的 icon 效果，清爽的页面设计

### 通用规范
- 使用英文注释和变量命名
- 提交信息使用约定式提交格式
- 代码通过 ESLint 检查，确保无报错
- JWT 进行前后端鉴权

## 技术栈说明

### 后端核心依赖
- Django 5.2.6 - Web 框架
- Django REST Framework - API 开发
- djangorestframework-simplejwt - JWT 认证
- requests - HTTP 请求库
- pyecharts - 图表生成
- 阿里云 SDK (最新版，兼容 Python 3.12)
- Let's Encrypt SDK (最新版，兼容 Python 3.12)
- 注意：使用 `pip install` 安装，不限定版本

### 前端核心依赖 (使用最新版)
- Vue 3.5.18 - 前端框架
- TypeScript 5.8 - 类型系统
- Vite 7.0.6 - 构建工具
- Vue Router 4.5.1 - 路由管理
- Pinia 3.0.3 - 状态管理
- Element Plus - UI 组件库
- ECharts - 图表组件
- Vue I18n - 国际化支持
- Node.js 22 - 运行环境

### 数据库与部署
- SQLite3 (开发环境)
- PostgreSQL (生产环境)
- 支持 SSH 远程部署

## 用户认证系统

### 支持的登录方式
1. **用户名密码登录** (优先实现)
2. **企业微信登录**
3. **钉钉登录** 
4. **飞书登录**

### 用户模型设计
- 系统内置用户系统 (Django User)
- 企业微信用户模型 (关联到内置用户)
- 钉钉用户模型 (关联到内置用户)
- 飞书用户模型 (关联到内置用户)
- 保存用户信息：头像、手机号、昵称等

### JWT 认证流程
- 登录成功后返回 access_token 和 refresh_token
- 前端存储 token 并在请求头中携带
- 后端验证 token 有效性
- 提供用户信息获取接口

## SSL 证书管理功能

### 证书申请与管理
- 支持多个 CA 提供商：Let's Encrypt、阿里云、华为云、腾讯云
- 自动化证书申请和更新流程
- 支持多种证书格式：nginx、apache、tomcat等
- 域名验证 (HTTP/DNS 验证)
- 证书状态实时监控

### 证书部署功能
- 本地文件夹部署
- SSH 远程服务器部署
- 自动部署到用户指定目标文件夹
- 部署状态监控和日志记录

### 证书到期提醒
- 提前30天到期提醒
- 支持多种通知渠道：
  - 企业微信机器人
  - 飞书机器人
  - 钉钉机器人
  - 系统内消息通知

## 系统设置功能

### 平台集成配置
- 企业微信应用配置 (AppID、AppSecret、Token等)
- 飞书应用配置 (App ID、App Secret等)
- 钉钉应用配置 (AppKey、AppSecret等)
- 阿里云API配置 (AccessKey、SecretKey等)
- Let's Encrypt API配置

### 机器人通知配置
- 企业微信群机器人 Webhook
- 飞书群机器人 Webhook  
- 钉钉群机器人 Webhook
- 通知模板自定义

## API 设计规范
- 统一使用 `/api/v1/` 前缀
- 响应格式：`{code: number, message: string, data: any}`
- 错误码统一管理
- 支持分页：`{page: number, size: number, total: number, items: []}`
- 使用 JWT 进行身份认证
- 所有敏感 API 凭据加盐保存到数据库

## 前端组件开发规范
- 组件具有良好的复用性，使用 Element Plus 组件
- 使用 Props 和 Emits 进行父子组件通信
- 复杂状态使用 Pinia store 管理
- 支持国际化，自动识别浏览器语言
- 清爽的页面设计，丰富的 icon 效果
- 登录后自动获取用户信息

## 环境配置要求
- 前端需要4个环境配置文件：
  - `.env.development` - 开发环境
  - `.env.test` - 测试环境  
  - `.env.staging` - 预发布环境
  - `.env.production` - 生产环境
- Django 支持国际化配置
- Python 命令执行前需激活虚拟环境

## 开发优先级
1. **第一阶段**: 用户名密码登录功能
2. **第二阶段**: 企业微信登录集成
3. **第三阶段**: 钉钉登录集成  
4. **第四阶段**: 飞书登录集成
5. **后续阶段**: SSL证书管理核心功能
- 数据库查询优化
