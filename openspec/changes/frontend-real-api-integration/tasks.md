# 前端真实API数据集成 - 任务分解

## API服务层 (4个任务)

### FE-API-001: 创建基础API配置
**描述**: 创建axios实例和基础API配置
**优先级**: 高
**预计时间**: 30分钟

**交付物**:
- `frontend/src/services/api.ts`
- axios实例配置
- baseURL设置
- 请求/响应拦截器
- 超时配置
- 错误处理

**实现内容**:
```typescript
- API_BASE_URL: http://localhost:8000
- timeout: 15000ms
- 请求拦截: 添加通用headers
- 响应拦截: 统一错误处理
```

---

### FE-API-002: 创建API类型定义
**描述**: 定义所有API请求和响应的TypeScript类型
**优先级**: 高
**预计时间**: 45分钟

**交付物**:
- `frontend/src/services/types.ts`
- DashboardStats接口
- MilestoneAchievement接口
- TrendPoint接口
- HeatmapData接口
- DashboardOverview接口
- ApiError接口

**类型定义**:
```typescript
interface DashboardStats {
  today_commits: number;
  today_additions: number;
  today_deletions: number;
  week_commits: number;
  week_additions: number;
  week_deletions: number;
  month_commits: number;
  month_additions: number;
  month_deletions: number;
  streak_days: number;
  active_language: string;
  work_hours: number;
  total_repositories: number;
  code_lines: number;
  last_updated: string;
}
// ... 其他接口
```

---

### FE-API-003: 实现仪表板API服务
**描述**: 封装所有仪表板相关的API调用
**优先级**: 高
**预计时间**: 1小时

**交付物**:
- `frontend/src/services/dashboard.ts`
- getDashboardOverview()
- getDashboardStats()
- getMilestones()
- getTrendData()
- getHeatmapData()

**实现内容**:
```typescript
export const dashboardApi = {
  getOverview: (userId: number) => 
    api.get<DashboardOverview>(`/api/v1/dashboard/overview?user_id=${userId}`),
  
  getStats: (userId: number) =>
    api.get<DashboardStats>(`/api/v1/dashboard/stats?user_id=${userId}`),
  
  // ... 其他方法
}
```

---

### FE-API-004: 实现调度器API服务
**描述**: 封装定时任务管理的API调用
**优先级**: 中
**预计时间**: 45分钟

**交付物**:
- `frontend/src/services/scheduler.ts`
- getSchedulerStatus()
- listJobs()
- createJob()
- deleteJob()
- triggerJob()

**实现内容**:
```typescript
export const schedulerApi = {
  getStatus: () => 
    api.get('/api/v1/scheduler/status'),
  
  listJobs: () =>
    api.get('/api/v1/scheduler/jobs'),
  
  createJob: (job: JobCreate) =>
    api.post('/api/v1/scheduler/jobs', job),
  
  // ... 其他方法
}
```

---

## Pinia Store更新 (3个任务)

### FE-STORE-001: 更新stats store集成API
**描述**: 修改stats store使用真实API替换模拟数据
**优先级**: 高
**预计时间**: 1.5小时

**修改文件**:
- `frontend/src/stores/stats.ts`

**实现内容**:
- 添加loading状态
- 添加error状态  
- 实现fetchDashboardData action
- 实现refreshData action
- 移除所有硬编码模拟数据
- 使用dashboardApi调用

**示例代码**:
```typescript
const stats = defineStore('stats', {
  state: () => ({
    dashboard: null as DashboardOverview | null,
    loading: false,
    error: null as string | null,
    lastUpdated: null as Date | null
  }),
  
  actions: {
    async fetchDashboardData(userId: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const data = await dashboardApi.getOverview(userId);
        this.dashboard = data;
        this.lastUpdated = new Date();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
})
```

---

### FE-STORE-002: 更新user store集成API
**描述**: 修改user store使用真实用户数据
**优先级**: 中
**预计时间**: 30分钟

**修改文件**:
- `frontend/src/stores/user.ts`

**实现内容**:
- 从后端API获取用户信息
- 或从localStorage读取配置的username
- 添加setUser action
- 添加loading/error状态

---

### FE-STORE-003: 创建scheduler store
**描述**: 新建scheduler store管理定时任务
**优先级**: 低
**预计时间**: 45分钟

**新建文件**:
- `frontend/src/stores/scheduler.ts`

**实现内容**:
- jobs状态
- fetchJobs action
- createJob action
- deleteJob action
- triggerJob action

---

## UI组件集成 (3个任务)

### FE-UI-001: 添加加载状态组件
**描述**: 创建通用的加载状态显示组件
**优先级**: 高
**预计时间**: 30分钟

**交付物**:
- `frontend/src/components/LoadingSpinner.vue`
- 骨架屏组件（可选）

**实现内容**:
- 旋转动画
- 全屏遮罩（可选）
- 自定义大小
- 科技风样式

---

### FE-UI-002: 添加错误提示组件
**描述**: 创建错误提示和重试UI
**优先级**: 高
**预计时间**: 30分钟

**交付物**:
- `frontend/src/components/ErrorAlert.vue`

**实现内容**:
- 错误消息显示
- 重试按钮
- 关闭按钮
- 自动消失（可选）

---

### FE-UI-003: 更新DashboardView集成API
**描述**: 修改仪表板页面使用store的真实数据
**优先级**: 高
**预计时间**: 1小时

**修改文件**:
- `frontend/src/views/DashboardView.vue`

**实现内容**:
- onMounted调用fetchDashboardData
- 显示loading状态
- 显示error状态
- 添加刷新按钮
- 处理空数据状态

**示例代码**:
```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import { useStatsStore } from '@/stores/stats'

const statsStore = useStatsStore()

onMounted(async () => {
  await statsStore.fetchDashboardData(1) // 使用实际user_id
})
</script>

<template>
  <div v-if="statsStore.loading">
    <LoadingSpinner />
  </div>
  
  <div v-else-if="statsStore.error">
    <ErrorAlert 
      :message="statsStore.error" 
      @retry="statsStore.fetchDashboardData(1)" 
    />
  </div>
  
  <div v-else-if="statsStore.dashboard">
    <!-- 现有组件使用statsStore.dashboard数据 -->
  </div>
</template>
```

---

## 测试和优化 (3个任务)

### FE-TEST-001: API集成测试
**描述**: 测试所有API调用是否正常
**优先级**: 高
**预计时间**: 1小时

**测试内容**:
- 测试正常流程
- 测试错误处理
- 测试网络异常
- 测试超时处理
- 验证数据格式

---

### FE-TEST-002: CORS配置验证
**描述**: 确保跨域请求正常工作
**优先级**: 高
**预计时间**: 30分钟

**测试内容**:
- 验证OPTIONS预检请求
- 验证实际数据请求
- 检查响应headers
- 测试不同端口访问

---

### FE-OPT-001: 实现数据缓存
**描述**: 添加数据缓存减少API调用
**优先级**: 中
**预计时间**: 1小时

**实现内容**:
- localStorage缓存
- 缓存过期策略
- 缓存更新逻辑
- 强制刷新选项

---

## 任务优先级排序

### Phase 1 - 基础设施 (4个任务, 2.5小时)
1. FE-API-001: 创建基础API配置
2. FE-API-002: 创建API类型定义
3. FE-API-003: 实现仪表板API服务
4. FE-UI-001: 添加加载状态组件

### Phase 2 - Store集成 (2个任务, 2小时)
5. FE-STORE-001: 更新stats store集成API
6. FE-UI-002: 添加错误提示组件

### Phase 3 - UI更新 (1个任务, 1小时)
7. FE-UI-003: 更新DashboardView集成API

### Phase 4 - 测试优化 (3个任务, 2.5小时)
8. FE-TEST-001: API集成测试
9. FE-TEST-002: CORS配置验证
10. FE-OPT-001: 实现数据缓存

### Phase 5 - 扩展功能 (3个任务, 2小时)
11. FE-STORE-002: 更新user store集成API
12. FE-API-004: 实现调度器API服务
13. FE-STORE-003: 创建scheduler store

---

## 预计总工时

| 阶段 | 任务数 | 预计时间 |
|------|--------|----------|
| Phase 1 | 4 | 2.5小时 |
| Phase 2 | 2 | 2小时 |
| Phase 3 | 1 | 1小时 |
| Phase 4 | 3 | 2.5小时 |
| Phase 5 | 3 | 2小时 |
| **总计** | **13** | **10小时** |

---

## 关键技术点

### 1. 错误处理策略
```typescript
try {
  const data = await api.get('/endpoint')
  return data
} catch (error) {
  if (error.response) {
    // 服务器返回错误响应
    throw new Error(error.response.data.detail)
  } else if (error.request) {
    // 请求已发出但无响应
    throw new Error('网络连接失败，请检查后端服务')
  } else {
    // 其他错误
    throw new Error('请求失败: ' + error.message)
  }
}
```

### 2. 类型安全
- 所有API响应必须有类型定义
- 使用TypeScript严格模式
- Store状态必须类型化

### 3. 性能优化
- 避免重复请求
- 使用请求防抖
- 实施数据缓存
- 懒加载大数据集

---

## 验收标准

**必须满足**:
1. ✅ 所有模拟数据已移除
2. ✅ 所有页面显示真实API数据
3. ✅ 加载状态正常显示
4. ✅ 错误处理完善
5. ✅ TypeScript类型完整
6. ✅ 无console错误
7. ✅ CORS问题已解决
8. ✅ API调用成功率100%

**可选优化**:
- ⚪ 数据缓存实现
- ⚪ 骨架屏加载
- ⚪ 请求重试机制
- ⚪ 离线提示