# 项目上下文

## Purpose
GitHub仓库监控工具 - 一个用于追踪和分析GitHub仓库活动和统计数据的全栈应用程序。该工具帮助开发者和团队监控仓库指标、活动趋势和贡献者统计信息。

## 技术栈
- **后端**: Python 3.9+, FastAPI
- **前端**: Vue.js 3.x, TypeScript
- **数据库**: PostgreSQL (用于持久化存储), Redis (用于缓存)
- **API集成**: GitHub REST API, GitHub GraphQL API
- **部署**: Docker, Docker Compose
- **测试**: pytest (后端), Vitest (前端)

## 项目约定

### 代码风格
- **Python**: 遵循PEP 8规范，使用Black进行格式化，最大行长88字符
- **TypeScript/Vue**: 遵循Vue 3 Composition API风格指南，使用Prettier格式化
- **命名约定**:
  - Python: snake_case用于函数和变量，PascalCase用于类
  - TypeScript: camelCase用于函数和变量，PascalCase用于组件和类
  - 文件名: kebab-case用于Vue组件，snake_case用于Python模块
- **注释**: 使用中文注释，但代码标识符使用英文

### 架构模式
- **后端**: 
  - 分层架构：API路由 → 服务层 → 数据访问层
  - 依赖注入用于服务和仓库
  - RESTful API设计原则
- **前端**:
  - 组件化架构，Composition API优先
  - Pinia用于状态管理
  - 路由懒加载优化性能
- **API集成**:
  - 速率限制处理和重试机制
  - 数据缓存策略（Redis）减少API调用

### 测试策略
- **单元测试**: 核心业务逻辑必须有单元测试覆盖
- **集成测试**: API端点和数据库交互需要集成测试
- **E2E测试**: 关键用户流程需要端到端测试
- **覆盖率目标**: 最低80%代码覆盖率
- **测试数据**: 使用fixtures和工厂模式生成测试数据

### Git 工作流
- **分支策略**: 
  - `main`: 生产就绪代码
  - `develop`: 开发分支
  - `feature/*`: 功能分支
  - `bugfix/*`: Bug修复分支
  - `hotfix/*`: 紧急修复分支
- **提交约定**: 
  - 使用Conventional Commits格式
  - 类型: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - 示例: `feat: add repository star count tracking`
- **PR要求**: 
  - 需要至少一个审查批准
  - 所有测试必须通过
  - 代码覆盖率不能下降

## 领域上下文

### GitHub API限制
- **未认证请求**: 60次/小时
- **已认证请求**: 5000次/小时
- **GraphQL API**: 5000点数/小时
- 需要实现智能缓存和请求批处理以避免超限

### 监控指标
- **仓库指标**: Stars, Forks, Watchers, Issues, Pull Requests
- **活动数据**: Commits, Contributors, Code Frequency
- **趋势分析**: 时间序列数据，增长率，活跃度评分

### 数据刷新策略
- **热门仓库**: 每小时更新
- **普通仓库**: 每6小时更新
- **低活跃仓库**: 每24小时更新
- 用户可以手动触发即时刷新（有频率限制）

## 重要约束

### 技术约束
- GitHub API速率限制必须严格遵守
- 响应时间要求: API端点 < 500ms (P95)
- 数据库查询优化: 避免N+1查询问题
- 缓存策略: Redis TTL根据数据重要性设置

### 业务约束
- 免费用户最多监控5个仓库
- 付费用户最多监控50个仓库
- 历史数据保留期: 免费用户30天，付费用户1年

### 安全约束
- GitHub Token必须加密存储
- 敏感配置使用环境变量
- API端点需要认证和授权
- 输入验证防止注入攻击

## 外部依赖

### GitHub API
- REST API v3: https://api.github.com
- GraphQL API v4: https://api.github.com/graphql
- Webhooks用于实时更新（可选功能）

### 数据存储
- PostgreSQL 13+: 主数据存储
- Redis 6+: 缓存和会话管理

### 监控和日志
- 应用日志: 结构化日志（JSON格式）
- 错误跟踪: 待集成（Sentry或类似工具）
- 性能监控: 待集成（Prometheus + Grafana）

### 第三方服务
- 邮件服务: 用于通知（待集成）
- 任务队列: Celery + Redis（用于后台任务）
