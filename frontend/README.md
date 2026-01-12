# GitHub Monitor Frontend

现代科技风格的个人代码追踪系统前端应用

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 3状态管理
- **Vue Router** - 官方路由
- **ECharts** - 数据可视化（即将集成）

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

应用将在 http://localhost:5173 启动

### 构建生产版本

```bash
npm run build
```

### 类型检查

```bash
npm run type-check
```

## 项目结构

```
frontend/
├── src/
│   ├── components/     # 可复用组件
│   │   ├── AppNav.vue          # 导航栏
│   │   ├── TechCard.vue        # 科技风格卡片
│   │   ├── TechButton.vue      # 科技风格按钮
│   │   ├── StatCard.vue        # 统计卡片
│   │   └── CountUp.vue         # 数字动画
│   ├── views/          # 页面组件
│   │   ├── DashboardView.vue   # 仪表盘
│   │   ├── TrendsView.vue      # 趋势分析
│   │   └── AchievementsView.vue # 成就系统
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia状态管理
│   ├── styles/         # 全局样式
│   ├── App.vue         # 根组件
│   └── main.ts         # 入口文件
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 设计系统

### 配色方案

采用现代科技风格，柔和易读的配色：

- **主色调**: 蓝紫色渐变 (#4A90E2 → #7C5CDB)
- **成功色**: 绿色 (#52C41A)
- **警告色**: 橙色 (#FA8C16)
- **危险色**: 红色 (#F5222D)

### 组件风格

- 柔和的发光效果
- 流畅的过渡动画
- 响应式设计
- 深色主题优化

## 开发规范

- 使用 TypeScript 进行类型检查
- 遵循 Vue 3 Composition API 风格
- 组件命名使用 PascalCase
- 变量和函数使用 camelCase
- 注释使用中文

## 待实现功能

- [ ] ECharts 图表集成
- [ ] API 服务层
- [ ] 状态管理完善
- [ ] 数据可视化组件
- [ ] 更多交互动画
- [ ] 移动端优化

## 许可证

MIT