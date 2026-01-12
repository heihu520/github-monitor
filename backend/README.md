# GitHub Monitor Backend API

个人代码开发洞察系统 - FastAPI后端服务

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并配置：

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或使用启动脚本（Windows）:
```bash
./start_server.bat
```

### 4. 访问API文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## API端点

### 个人仪表板 (Dashboard)

**基础路径**: `/api/v1/dashboard`

#### 1. 获取仪表板总览
```
GET /api/v1/dashboard/overview?user_id=demo-user
```

返回完整的仪表板数据，包括：
- 统计数据（今日/本周/本月提交、代码量）
- 里程碑成就列表
- 最近7天提交趋势
- 90天编码活跃度热力图

#### 2. 获取统计数据
```
GET /api/v1/dashboard/stats?user_id=demo-user
```

仅返回统计数据，响应更快。

#### 3. 获取里程碑成就
```
GET /api/v1/dashboard/milestones?user_id=demo-user
```

返回用户的成就列表和进度。

#### 4. 获取提交趋势
```
GET /api/v1/dashboard/trend?user_id=demo-user&days=7
```

返回指定天数的提交趋势数据。

#### 5. 获取活跃度热力图
```
GET /api/v1/dashboard/heatmap?user_id=demo-user&days=90
```

返回类似GitHub贡献图的热力图数据。

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   └── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── dashboard.py  # 仪表板API路由
│   ├── models/
│   │   ├── __init__.py
│   │   └── dashboard.py     # 数据模型
│   └── services/
│       ├── __init__.py
│       └── dashboard_service.py  # 业务逻辑
├── requirements.txt         # 项目依赖
├── .env.example            # 环境变量示例
└── README.md               # 项目文档
```

## 技术栈

- **FastAPI**: 现代化的Python Web框架
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI服务器
- **MySQL**: 主数据库
  - 用户: hadoop
  - 密码: hadoop
  - 数据库: github_monitor
- **Redis**: 缓存层（计划中）

## 开发指南

### 添加新的API端点

1. 在 `app/models/` 创建数据模型
2. 在 `app/services/` 创建业务逻辑
3. 在 `app/api/v1/` 创建路由
4. 在 `app/api/v1/__init__.py` 注册路由

### 代码规范

- 使用Black进行代码格式化
- 遵循PEP 8命名规范
- 添加类型注解
- 编写文档字符串

## 当前状态

**APCI-BE-001**: ✅ 个人仪表板数据聚合API已完成

已实现功能：
- ✅ 仪表板总览API
- ✅ 统计数据API
- ✅ 里程碑成就API
- ✅ 提交趋势API
- ✅ 活跃度热力图API
- ✅ 完整的数据模型定义
- ✅ 模拟数据服务

待开发功能：
- ⏳ 数据库集成
- ⏳ Redis缓存
- ⏳ GitHub API集成
- ⏳ 用户认证
- ⏳ 数据持久化

## License

MIT