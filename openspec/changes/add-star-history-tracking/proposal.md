# Change: 添加仓库星标历史追踪功能

## Why
当前系统只能显示仓库的当前星标数量，无法追踪历史变化趋势。用户需要了解仓库的增长趋势来评估项目的受欢迎程度和发展轨迹。添加星标历史追踪功能可以：
- 帮助用户识别热门项目和趋势
- 提供可视化的增长曲线
- 支持对比多个仓库的星标增长情况

## What Changes
- 添加星标历史数据采集功能
- 实现星标数据的时间序列存储
- 创建星标历史查询API端点
- 在前端展示星标增长曲线图
- 添加定时任务定期采集星标数据
- 支持导出星标历史数据（CSV格式）

## Impact
- 影响的规范：
  - `repository-monitoring`（新增功能）
  - `data-collection`（新增功能）
  - `api-endpoints`（新增功能）
- 影响的代码：
  - 后端：`app/services/github_collector.py`，`app/models/star_history.py`，`app/api/v1/repositories.py`
  - 前端：`src/components/StarHistoryChart.vue`，`src/services/api.ts`
  - 数据库：新增`star_history`表
  - 任务调度：`app/tasks/star_collector.py`
- 性能影响：
  - 数据库存储增加（每个仓库每天约100字节）
  - 额外的GitHub API调用（每个仓库每天1次）
- 用户影响：
  - 免费用户：查看最近30天历史
  - 付费用户：查看完整历史（最多1年）