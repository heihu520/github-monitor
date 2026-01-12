# 🌟 赛博朋克风格UI设计指南

打造极具未来感和科技感的个人代码追踪系统界面

---

## 🎨 配色方案

### 主色调系统

```css
/* 霓虹色彩 - 主要交互和数据展示 */
--neon-blue: #00F0FF;        /* 霓虹蓝 - 主色调 */
--neon-purple: #B300FF;      /* 霓虹紫 - 次要色 */
--neon-pink: #FF006E;        /* 霓虹粉 - 强调色 */
--neon-green: #39FF14;       /* 霓虹绿 - 成功/正向 */
--neon-yellow: #FFFF00;      /* 霓虹黄 - 警告 */
--neon-orange: #FF9500;      /* 霓虹橙 - 提示 */
--neon-red: #FF0040;         /* 霓虹红 - 错误/危险 */

/* 背景色系 - 深空赛博氛围 */
--bg-primary: #0A0E27;       /* 深空黑 - 主背景 */
--bg-secondary: #1A1F3A;     /* 深蓝黑 - 卡片背景 */
--bg-tertiary: #252B4A;      /* 中蓝黑 - 悬浮元素 */
--bg-overlay: rgba(10, 14, 39, 0.95);  /* 半透明遮罩 */

/* 文字色系 */
--text-primary: #E8F1F5;     /* 冷白 - 主要文字 */
--text-secondary: #8B9DC3;   /* 淡青灰 - 次要文字 */
--text-tertiary: #5A6A8A;    /* 灰蓝 - 辅助文字 */
--text-disabled: #3A4A6A;    /* 深灰蓝 - 禁用状态 */

/* 边框和线条 */
--border-glow: rgba(0, 240, 255, 0.3);   /* 发光边框 */
--border-subtle: rgba(139, 157, 195, 0.2); /* 微妙分割线 */
--grid-line: rgba(0, 240, 255, 0.1);     /* 网格线 */

/* 渐变预设 */
--gradient-primary: linear-gradient(135deg, #00F0FF 0%, #B300FF 100%);
--gradient-success: linear-gradient(135deg, #39FF14 0%, #00F0FF 100%);
--gradient-warning: linear-gradient(135deg, #FFFF00 0%, #FF9500 100%);
--gradient-danger: linear-gradient(135deg, #FF006E 0%, #FF0040 100%);
--gradient-bg: linear-gradient(180deg, #0A0E27 0%, #1A1F3A 100%);
```

### 发光效果系统

```css
/* 霓虹发光效果 - Box Shadow */
.glow-blue {
  box-shadow: 
    0 0 10px rgba(0, 240, 255, 0.5),
    0 0 20px rgba(0, 240, 255, 0.3),
    0 0 30px rgba(0, 240, 255, 0.1);
}

.glow-purple {
  box-shadow: 
    0 0 10px rgba(179, 0, 255, 0.5),
    0 0 20px rgba(179, 0, 255, 0.3),
    0 0 30px rgba(179, 0, 255, 0.1);
}

.glow-green {
  box-shadow: 
    0 0 10px rgba(57, 255, 20, 0.5),
    0 0 20px rgba(57, 255, 20, 0.3);
}

.glow-pink {
  box-shadow: 
    0 0 10px rgba(255, 0, 110, 0.5),
    0 0 20px rgba(255, 0, 110, 0.3);
}

/* 文字发光效果 - Text Shadow */
.text-glow-neon {
  text-shadow:
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 30px currentColor;
}

.text-glow-subtle {
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}
```

---

## 🎯 图标系统

### 统计数据图标

```
功能                 图标      颜色          说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
提交数              📊        霓虹蓝        发光柱状图，带脉动
代码量              💻        霓虹紫        代码符号</>，带扫描线
连续天数            🔥        霓虹橙→红     火焰，带跳动动画
工作时长            ⚡        霓虹黄        闪电，带电流效果
完成率              🎯        霓虹绿        靶心，带环形进度
成就数              🌟        金色渐变      星星，带闪烁
生产力              🚀        蓝紫渐变      火箭，带尾焰
增长率              📈        绿色/红色     箭头，带流光
活跃度              💫        青蓝色        星光，带扩散
专注时长            🧠        紫色          大脑，带脉冲
休息时间            😴        淡蓝色        月亮，带呼吸效果
```

### 编程语言图标

```
语言                图标      颜色代码      备注
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Python              🐍        #39FF14       蛇形代码，霓虹绿
JavaScript          ⚡        #FFFF00       闪电JS，霓虹黄
TypeScript          🔷        #00F0FF       蓝色方块，带TS标记
React               ⚛️        #00F0FF       原子符号，青蓝色
Vue.js              💚        #39FF14       V字标志，翠绿色
Rust                🦀        #FF9500       螃蟹，橙红色
Java                ☕        #FF6B35       咖啡杯，橙色
Go                  🎯        #00F0FF       地鼠，青色
C/C++               🔷        #B300FF       六边形，紫色
Ruby                💎        #FF006E       宝石，红色
PHP                 🐘        #B300FF       大象，紫色
Swift               🦅        #FF9500       鸟，橙色
Kotlin              🔶        #FF006E       K字母，品红
HTML/CSS            🎨        gradient      调色板，彩虹色
SQL                 🗄️        #8B9DC3       数据库，灰蓝
Markdown            📝        #E8F1F5       笔记，白色
```

### 时间段图标（带氛围色）

```
时段                图标      颜色渐变              氛围
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
凌晨 (00-06)        🌙        深蓝→淡蓝            安静
清晨 (06-09)        🌅        橙→黄→粉            朝气
上午 (09-12)        ☀️        黄→金              高效
中午 (12-14)        🌞        金→橙              活力
下午 (14-18)        ☀️        黄→橙              稳定
傍晚 (18-20)        🌆        橙→紫→蓝           过渡
晚上 (20-23)        🌃        蓝→紫              放松
深夜 (23-00)        🌙        紫→深蓝            专注
```

### 成就等级图标

```
等级                图标      颜色效果                  解锁条件示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
新手                🌱        灰白，轮廓线            0-10次提交
初学                🌿        淡绿，微光              10-50次
入门                🌳        翠绿，发光              50-100次
熟练                ⭐        金黄，闪烁              100-500次
精通                💫        蓝紫渐变，光晕          500-1000次
专家                🏆        金色，强光              1000-5000次
大师                👑        彩虹光，粒子效果        5000+次
传奇                ⚡💎      多色炫光，爆发          特殊成就
```

### 状态和操作图标

```
状态/操作           图标      颜色          动画效果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
成功                ✅        霓虹绿        脉动
警告                ⚠️        霓虹黄        闪烁（慢）
错误                ❌        霓虹红        抖动
加载中              🔄        蓝紫渐变      旋转
同步中              🔃        霓虹蓝        环形旋转
已完成              ✔️        霓虹绿        勾选动画
进行中              ▶️        霓虹蓝        右移
暂停                ⏸️        霓虹黄        静止
锁定                🔒        灰色          无动画
解锁                🔓        金色          开启动画
收藏                ⭐        金色          填充切换
设置                ⚙️        霓虹蓝        旋转（慢）
刷新                🔄        霓虹青        旋转
导出                📤        霓虹紫        上移
导入                📥        霓虹绿        下移
删除                🗑️        霓虹红        淡出
编辑                ✏️        霓虹蓝        无动画
查看                👁️        霓虹青        眨眼
复制                📋        霓虹蓝        复制动画
分享                🔗        霓虹紫        扩散
```

---

## 📐 UI组件样式

### 1. 霓虹发光卡片

```html
<div class="cyber-card">
  <div class="card-header">
    <span class="icon">📊</span>
    <h3 class="title">今日统计</h3>
  </div>
  <div class="card-body">
    <div class="stat-item">
      <span class="value">42</span>
      <span class="label">提交次数</span>
    </div>
  </div>
</div>
```

```css
.cyber-card {
  background: linear-gradient(
    135deg,
    rgba(26, 31, 58, 0.8) 0%,
    rgba(37, 43, 74, 0.6) 100%
  );
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 8px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  
  /* 霓虹发光 */
  box-shadow: 
    0 0 20px rgba(0, 240, 255, 0.2),
    inset 0 0 20px rgba(0, 240, 255, 0.05);
  
  /* 背景网格 */
  background-image: 
    linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
  
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cyber-card:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 8px 30px rgba(0, 240, 255, 0.4),
    inset 0 0 30px rgba(0, 240, 255, 0.1);
  border-color: rgba(0, 240, 255, 0.6);
}

/* 扫描线动画 */
.cyber-card::before {
  content: '';
  position: absolute;
  top: -100%;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(0, 240, 255, 0.1) 50%,
    transparent 100%
  );
  animation: scan 3s linear infinite;
}

@keyframes scan {
  0% { top: -100%; }
  100% { top: 100%; }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.icon {
  font-size: 32px;
  filter: drop-shadow(0 0 8px currentColor);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.title {
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--neon-blue);
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
  margin: 0;
}

.value {
  font-family: 'Share Tech Mono', monospace;
  font-size: 48px;
  font-weight: 700;
  background: linear-gradient(135deg, #00F0FF, #B300FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
}
```

### 2. 赛博朋克按钮

```html
<button class="cyber-button primary">
  <span class="button-icon">🚀</span>
  <span class="button-text">启动分析</span>
  <span class="button-glow"></span>
</button>
```

```css
.cyber-button {
  position: relative;
  padding: 12px 32px;
  font-family: 'Rajdhani', sans-serif;
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #fff;
  background: linear-gradient(135deg, #00F0FF, #B300FF);
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  
  /* 发光效果 */
  box-shadow: 
    0 0 20px rgba(0, 240, 255, 0.4),
    inset 0 0 10px rgba(255, 255, 255, 0.1);
}

.cyber-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.5s;
}

.cyber-button:hover::before {
  left: 100%;
}

.cyber-button:hover {
  transform: scale(1.05);
  box-shadow: 
    0 0 30px rgba(0, 240, 255, 0.6),
    inset 0 0 20px rgba(255, 255, 255, 0.2);
}

.cyber-button:active {
  transform: scale(0.95);
}

.button-icon {
  margin-right: 8px;
  font-size: 20px;
}

/* 按钮变体 */
.cyber-button.secondary {
  background: linear-gradient(135deg, #B300FF, #FF006E);
}

.cyber-button.success {
  background: linear-gradient(135deg, #39FF14, #00F0FF);
}

.cyber-button.ghost {
  background: transparent;
  border: 2px solid var(--neon-blue);
  box-shadow: 
    0 0 10px rgba(0, 240, 255, 0.3),
    inset 0 0 10px rgba(0, 240, 255, 0.05);
}
```

### 3. 霓虹进度条

```html
<div class="cyber-progress">
  <div class="progress-track">
    <div class="progress-fill" style="width: 75%;"></div>
    <div class="progress-glow"></div>
  </div>
  <span class="progress-text">75%</span>
</div>
```

```css
.cyber-progress {
  position: relative;
}

.progress-track {
  height: 12px;
  background: rgba(26, 31, 58, 0.8);
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00F0FF, #B300FF);
  border-radius: 6px;
  position: relative;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  
  box-shadow: 
    0 0 20px rgba(0, 240, 255, 0.6),
    inset 0 0 10px rgba(255, 255, 255, 0.2);
}

/* 流光效果 */
.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 200%; }
}

.progress-text {
  position: absolute;
  right: 0;
  top: -24px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 14px;
  font-weight: 700;
  color: var(--neon-blue);
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}
```

### 4. 霓虹标签徽章

```html
<span class="cyber-badge feat">
  <span class="badge-icon">✨</span>
  <span class="badge-text">功能</span>
</span>
```

```css
.cyber-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: 12px;
  border: 1px solid currentColor;
  background: rgba(0, 240, 255, 0.1);
  color: var(--neon-blue);
  box-shadow: 
    0 0 10px currentColor,
    inset 0 0 5px rgba(255, 255, 255, 0.1);
}

.cyber-badge.feat { 
  color: #00F0FF; 
  background: rgba(0, 240, 255, 0.1);
}

.cyber-badge.fix { 
  color: #39FF14;
  background: rgba(57, 255, 20, 0.1);
}

.cyber-badge.docs { 
  color: #B300FF;
  background: rgba(179, 0, 255, 0.1);
}

.cyber-badge.test { 
  color: #FFFF00;
  background: rgba(255, 255, 0, 0.1);
}

.badge-icon {
  font-size: 10px;
}
```

---

## 🎬 动画效果库

### 入场动画

```css
/* 淡入 + 上移 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 霓虹闪现 */
@keyframes neonFlicker {
  0%, 100% { opacity: 1; }
  10% { opacity: 0.8; }
  20% { opacity: 1; }
  30% { opacity: 0.9; }
  40% { opacity: 1; }
}

/* 脉冲发光 */
@keyframes glowPulse {
  0%, 100% {
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 240, 255, 0.8);
  }
}

/* 扫描线 */
@keyframes scanLine {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

/* 数字滚动 */
@keyframes numberRoll {
  0% { transform: translateY(0); }
  100% { transform: translateY(-100%); }
}
```

---

## 📱 响应式断点

```css
/* 超大屏 */
@media (min-width: 1920px) {
  .container { max-width: 1800px; }
  .cyber-card { padding: 32px; }
  h1 { font-size: 48px; }
}

/* 桌面 */
@media (min-width: 1200px) and (max-width: 1919px) {
  .container { max-width: 1140px; }
  .cyber-card { padding: 24px; }
}

/* 平板横屏 */
@media (min-width: 992px) and (max-width: 1199px) {
  .container { max-width: 960px; }
  .cyber-card { padding: 20px; }
}

/* 平板竖屏 */
@media (min-width: 768px) and (max-width: 991px) {
  .container { max-width: 720px; }
  .cyber-card { padding: 16px; }
  /* 简化发光效果 */
  .cyber-card { box-shadow: 0 0 10px rgba(0, 240, 255, 0.2); }
}

/* 手机 */
@media (max-width: 767px) {
  .container { width: 100%; padding: 16px; }
  .cyber-card { padding: 12px; }
  /* 关闭背景动画 */
  .cyber-card::before { display: none; }
  /* 减少发光 */
  .cyber-card { box-shadow: 0 0 5px rgba(0, 240, 255, 0.2); }
}
```

---

## 🎯 使用示例

### 完整页面布局示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌟 个人代码追踪 - Cyberpunk Dashboard</title>
  <link rel="stylesheet" href="cyberpunk.css">
</head>
<body class="cyber-theme">
  <!-- 背景效果 -->
  <div class="cyber-bg">
    <div class="grid-overlay"></div>
    <div class="glow-particles"></div>
  </div>
  
  <!-- 主容器 -->
  <div class="container">
    <!-- 顶部导航 -->
    <nav class="cyber-nav">
      <div class="nav-logo">
        <span class="logo-icon">💻</span>
        <span class="logo-text">CODE TRACKER</span>
      </div>
      <div class="nav-menu">
        <a href="#" class="nav-item active">
          <span class="icon">📊</span>
          <span>仪表盘</span>
        </a>
        <a href="#" class="nav-item">
          <span class="icon">📈</span>
          <span>趋势</span>
        </a>
        <a href="#" class="nav-item">
          <span class="icon">🏆</span>
          <span>成就</span>
        </a>
      </div>
    </nav>
    
    <!-- 统计卡片网格 -->
    <div class="stats-grid">
      <div class="cyber-card">
        <div class="stat-header">
          <span class="icon">📊</span>
          <h3>今日提交</h3>
        </div>
        <div class="stat-value">
          <span class="number">8</span>
          <span class="trend up">+25%</span>
        </div>
      </div>
      
      <div class="cyber-card">
        <div class="stat-header">
          <span class="icon">💻</span>
          <h3>代码量</h3>
        </div>
        <div class="stat-value">
          <span class="number">1,234</span>
          <span class="label">lines</span>
        </div>
      </div>
      
      <div class="cyber-card">
        <div class="stat-header">
          <span class="icon">🔥</span>
          <h3>连续天数</h3>
        </div>
        <div class="stat-value">
          <span class="number">42</span>
          <span class="label">days</span>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="chart-container cyber-card">
      <h3 class="chart-title">
        <span class="icon">📈</span>
        提交趋势
      </h3>
      <div id="commit-chart"></div>
    </div>
  </div>
</body>
</html>
```

---

## 💡 设计原则

### 1. 视觉层次
- **主要信息**：大号字体 + 霓虹色 + 强发光
- **次要信息**：中号字体 + 淡色 + 微光
- **辅助信息**：小号字体 + 灰色 + 无发光

### 2. 色彩使用
- **蓝色系**：数据、信息、导航
- **绿色系**：成功、增长、正向指标
- **紫色系**：特殊、高级、VIP功能
- **红粉系**：警告、重要、需注意
- **黄橙系**：提示、中性、时间

### 3. 动画时机
- **加载**：1-2秒，炫酷但不过长
- **交互**：200-300ms，快速响应
- **状态变化**：400-500ms，明显但流畅
- **装饰**：2-4秒循环，微妙不打扰

### 4. 性能优先
- 优先使用CSS动画（GPU加速）
- 避免大面积复杂渐变
- 响应式关闭部分特效
- 懒加载非关键资源

---

## 🚀 技术实现建议

### Vue 3 + TypeScript 组件示例

```vue
<template>
  <div class="cyber-card" :class="{ 'is-loading': loading }">
    <div class="card-icon">{{ icon }}</div>
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <div class="card-value">
        <CountUp :value="value" />
      </div>
      <div v-if="trend" class="card-trend" :class="trendClass">
        {{ trendText }}
      </div>
    </div>
    <div class="scan-line"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import CountUp from '@/components/CountUp.vue'

interface Props {
  icon: string
  title: string
  value: number
  trend?: number
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const trendClass = computed(() => ({
  'trend-up': props.trend && props.trend > 0,
  'trend-down': props.trend && props.trend < 0
}))

const trendText = computed(() => {
  if (!props.trend) return ''
  const sign = props.trend > 0 ? '+' : ''
  return `${sign}${props.trend}%`
})
</script>

<style scoped>
/* 组件样式... */
</style>
```

---

*这份设计指南将持续更新，为打造极致赛博朋克体验提供支持！* 🌟