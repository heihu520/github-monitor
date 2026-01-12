# 🌟 GitHub Monitor - 个人代码追踪系统

<div align="center">

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.x-green.svg)

**一个赛博朋克风格的个人代码开发追踪和生产力分析工具**

[功能特性](#-功能特性) •
[技术栈](#-技术栈) •
[快速开始](#-快速开始) •
[文档](#-文档) •
[贡献指南](#-贡献指南)

</div>

---

## 📖 项目简介

GitHub Monitor 是一个为个人开发者设计的代码开发追踪和生产力分析工具。通过采集GitHub仓库的提交历史，提供多维度的数据分析和可视化，帮助开发者：

- 📊 **深入了解编码习惯** - 追踪每日、每周、每月的提交模式
- 🎯 **量化技能成长** - 可视化技术栈演进和语言使用趋势
- 🔥 **保持编码动力** - 游戏化激励系统，成就徽章和连续打卡
- 📈 **数据驱动提升** - AI洞察和个性化建议
- 🎨 **赛博朋克风格** - 极具未来感的霓虹色UI设计

## ✨ 功能特性

### 🎯 核心功能

- **多时间维度视图**
  - 📅 日视图 - 24小时精细化时间管理
  - 📊 周视图 - 习惯养成和周环比分析
  - 📈 月视图 - 日历热力图和月度统计
  - 🗓️ 年视图 - 年度编码回顾（类似Spotify Wrapped）

- **提交数据分析**
  - 自动采集GitHub提交历史
  - 智能提交类型分类（feat/fix/docs/test等）
  - 代码量统计（新增/删除行数）
  - 文件类型分析

- **多维度统计**
  - 按时间趋势分析
  - 按提交类型分布
  - 按贡献者排行
  - 按编程语言统计
  - 按工作时段分析

- **智能洞察**
  - AI驱动的个性化建议
  - 编码模式识别
  - 最佳工作时段推荐
  - 健康度监控（工作生活平衡）

- **游戏化激励**
  - 成就徽章系统（连续编码、里程碑等）
  - 开发者等级体系
  - 每日/每周挑战任务
  - 目标设定和追踪

### 🎨 视觉设计

- **赛博朋克风格UI**
  - 霓虹色配色方案（蓝/紫/粉/绿）
  - 发光效果和扫描线动画
  - 精美图标系统（100+图标）
  - 流畅的交互动画

- **数据可视化**
  - ECharts交互式图表
  - 折线图、柱状图、饼图、热力图
  - 实时数据更新动画
  - 自定义主题配色

- **响应式设计**
  - 桌面端完整体验
  - 平板端自适应布局
  - 移动端优化界面
  - 性能优先原则

## 🛠️ 技术栈

### 后端
- **Python 3.9+** - 核心语言
- **FastAPI** - 现代异步Web框架
- **MySQL** - 数据持久化存储
- **Redis** - 缓存和会话管理
- **Celery** - 后台任务调度
- **SQLAlchemy** - ORM框架

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全
- **Pinia** - 状态管理
- **ECharts** - 数据可视化
- **Vite** - 构建工具

### DevOps
- **Docker** - 容器化部署
- **Docker Compose** - 服务编排
- **GitHub Actions** - CI/CD
- **Nginx** - 反向代理

## 🚀 快速开始

### 前置要求

- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Redis 6.0+
- Git

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/你的用户名/github_monitor.git
cd github_monitor
```

2. **后端设置**
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写数据库和GitHub Token等配置

# 运行数据库迁移
alembic upgrade head

# 启动后端服务
uvicorn app.main:app --reload
```

3. **前端设置**
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

4. **访问应用**
- 前端：http://localhost:5173
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 使用Docker

```bash
# 构建和启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📚 文档

- [功能灵感集](FEATURE_INSPIRATIONS.md) - 完整的功能创意和设计理念
- [UI设计指南](UI_DESIGN_GUIDE.md) - 赛博朋克风格设计系统
- [OpenSpec规范](openspec/) - 项目规范和变更提案
  - [项目上下文](openspec/project.md)
  - [变更提案](openspec/changes/)
  - [功能规范](openspec/specs/)

## 🎯 路线图

### v0.1.0 - MVP版本 (当前)
- [x] 项目初始化和规范设计
- [x] UI设计系统定义
- [ ] 基础数据采集功能
- [ ] 核心可视化组件
- [ ] 日/周/月视图实现

### v0.2.0 - 增强版
- [ ] 智能洞察功能
- [ ] 游戏化激励系统
- [ ] 年度回顾报告
- [ ] 数据导出功能

### v0.3.0 - 高级版
- [ ] AI驱动分析
- [ ] 多仓库聚合
- [ ] 自定义仪表盘
- [ ] 移动端应用

### v1.0.0 - 正式版
- [ ] 性能优化
- [ ] 完整测试覆盖
- [ ] 用户文档完善
- [ ] 生产环境部署

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具变动

### 开发流程

本项目使用 [OpenSpec](https://github.com/openspec-dev/openspec) 进行规范驱动开发：

1. 查看现有规范和变更提案
2. 创建新的变更提案（如需要）
3. 实施功能并更新规范
4. 提交代码并请求审查

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

**Your Name**
- GitHub: [@你的用户名](https://github.com/你的用户名)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [ECharts](https://echarts.apache.org/) - 强大的数据可视化库
- [OpenSpec](https://github.com/openspec-dev/openspec) - 规范驱动开发工具

## 📧 联系方式

如有问题或建议，欢迎：
- 提交 Issue
- 发送邮件至：your.email@example.com
- 加入讨论群：[链接]

---

<div align="center">

**用数据讲述你的编码故事** 🚀

Made with ❤️ and ☕

</div>