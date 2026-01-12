## ADDED Requirements

### Requirement: 代码提交数据采集
系统 SHALL 从GitHub API采集仓库的提交历史数据，包括提交数量、提交者、提交时间、变更文件类型和代码行数变化。

#### Scenario: 每日定时采集提交数据
- **WHEN** 系统在每天凌晨2点执行定时任务
- **THEN** 系统 SHALL 采集过去24小时内所有监控仓库的新提交数据
- **AND** 系统 SHALL 解析每个提交的元数据（sha, author, message, timestamp）
- **AND** 系统 SHALL 统计每个提交的代码变更量（additions, deletions, files_changed）
- **AND** 系统 SHALL 将数据存储到MySQL数据库的`commits`表中

#### Scenario: 按需手动刷新提交数据
- **WHEN** 用户点击"立即刷新"按钮
- **THEN** 系统 SHALL 立即采集该仓库的最新提交数据
- **AND** 系统 SHALL 在30秒内完成数据刷新
- **AND** 系统 SHALL 返回采集到的新提交数量

#### Scenario: 处理大型仓库的分页采集
- **WHEN** 仓库有超过1000个提交需要采集
- **THEN** 系统 SHALL 使用分页方式分批采集
- **AND** 系统 SHALL 保存采集进度，支持断点续传
- **AND** 系统 SHALL 避免重复采集已存在的提交记录

### Requirement: 提交类型分类
系统 SHALL 根据提交信息和变更内容自动分类提交类型。

#### Scenario: 根据Conventional Commits自动分类
- **WHEN** 提交信息遵循Conventional Commits格式（如"feat:", "fix:", "docs:"）
- **THEN** 系统 SHALL 自动识别并标记提交类型
- **AND** 支持的类型包括：feat（功能）、fix（修复）、docs（文档）、style（样式）、refactor（重构）、test（测试）、chore（杂项）

#### Scenario: 根据文件变更智能分类
- **WHEN** 提交信息不包含类型标记
- **THEN** 系统 SHALL 分析变更的文件类型进行智能分类
- **AND** 如果主要修改`.md`或`.txt`文件，分类为文档类
- **AND** 如果主要修改测试文件（包含`test`或`spec`），分类为测试类
- **AND** 如果主要修改配置文件（`.json`, `.yml`, `.config.js`），分类为配置类
- **AND** 其他情况默认分类为代码类

#### Scenario: 人工修正提交分类
- **WHEN** 用户对自动分类不满意
- **THEN** 系统 SHALL 允许用户手动修改提交类型
- **AND** 系统 SHALL 保存用户的修正记录用于改进分类算法

### Requirement: 多维度提交统计分析
系统 SHALL 提供多个维度的提交数据统计和分析功能。

#### Scenario: 按时间维度查看提交趋势
- **WHEN** 用户访问提交趋势页面
- **THEN** 系统 SHALL 展示可选择的时间粒度：按天、按周、按月
- **AND** 系统 SHALL 显示该时间段内的总提交数、代码增加行数、代码删除行数
- **AND** 系统 SHALL 以折线图展示提交数量随时间的变化趋势
- **AND** 系统 SHALL 以堆叠柱状图展示代码增删量的对比

#### Scenario: 按提交类型统计分布
- **WHEN** 用户查看提交类型分析
- **THEN** 系统 SHALL 展示饼图显示各类型提交的占比（功能、修复、文档等）
- **AND** 系统 SHALL 显示每种类型的提交数量和百分比
- **AND** 系统 SHALL 支持点击饼图扇区查看该类型的详细提交列表

#### Scenario: 按贡献者统计排行
- **WHEN** 用户查看贡献者排行榜
- **THEN** 系统 SHALL 显示按提交数量排序的贡献者列表
- **AND** 系统 SHALL 展示每个贡献者的提交数、代码行数、主要贡献类型
- **AND** 系统 SHALL 支持按时间范围筛选（本周、本月、本季度、全部）
- **AND** 系统 SHALL 支持按指标排序（提交数、代码量、活跃天数）

#### Scenario: 按文件类型统计代码变更
- **WHEN** 用户查看文件类型分析
- **THEN** 系统 SHALL 识别并统计主要文件类型的变更（.py, .js, .vue, .md等）
- **AND** 系统 SHALL 显示每种文件类型的修改次数和代码变更量
- **AND** 系统 SHALL 以树状图或旭日图展示文件类型分布

#### Scenario: 按时段统计提交活跃度
- **WHEN** 用户查看提交活跃度热力图
- **THEN** 系统 SHALL 展示一周7天×24小时的提交热力图
- **AND** 系统 SHALL 用颜色深浅表示提交频率
- **AND** 系统 SHALL 帮助识别团队的工作时间模式

### Requirement: 可视化图表展示
系统 SHALL 提供丰富的可视化图表展示提交数据。

#### Scenario: 提交趋势折线图
- **WHEN** 用户查看提交趋势
- **THEN** 系统 SHALL 使用ECharts展示交互式折线图
- **AND** 图表 SHALL 支持缩放、拖拽和数据点悬停查看详情
- **AND** 图表 SHALL 支持对比多个仓库的提交趋势

#### Scenario: 代码变更柱状图
- **WHEN** 用户查看代码变更统计
- **THEN** 系统 SHALL 展示堆叠柱状图，区分代码增加和删除
- **AND** 绿色表示新增代码，红色表示删除代码
- **AND** 图表 SHALL 支持按时间范围筛选

#### Scenario: 提交类型饼图
- **WHEN** 用户查看提交分类
- **THEN** 系统 SHALL 展示交互式饼图
- **AND** 图表 SHALL 支持点击扇区查看详细列表
- **AND** 图表 SHALL 显示百分比标签

#### Scenario: 贡献者活跃度热力图
- **WHEN** 用户查看团队活跃度
- **THEN** 系统 SHALL 展示日历热力图，类似GitHub贡献图
- **AND** 图表 SHALL 用颜色深浅表示每日提交强度
- **AND** 图表 SHALL 支持悬停查看当日详细数据

### Requirement: 数据导出功能
系统 SHALL 支持将提交分析数据导出为多种格式。

#### Scenario: 导出CSV格式报表
- **WHEN** 用户点击"导出CSV"按钮
- **THEN** 系统 SHALL 生成包含所有提交记录的CSV文件
- **AND** CSV SHALL 包含字段：日期、提交SHA、作者、类型、描述、文件数、代码增加、代码删除
- **AND** 系统 SHALL 在5秒内完成导出并触发下载

#### Scenario: 导出Excel格式报表
- **WHEN** 用户点击"导出Excel"按钮
- **THEN** 系统 SHALL 生成包含多个工作表的Excel文件
- **AND** 工作表包括：原始数据、统计摘要、图表
- **AND** Excel SHALL 包含格式化的表格和内嵌图表

#### Scenario: 导出PDF分析报告
- **WHEN** 用户点击"生成PDF报告"按钮
- **THEN** 系统 SHALL 生成包含图表和统计数据的PDF报告
- **AND** 报告 SHALL 包含封面、时间范围、关键指标、各维度分析图表
- **AND** 报告 SHALL 支持自定义选择包含的分析维度

### Requirement: 数据筛选和搜索
系统 SHALL 提供灵活的数据筛选和搜索功能。

#### Scenario: 按时间范围筛选
- **WHEN** 用户选择时间范围
- **THEN** 系统 SHALL 提供快捷选项：最近7天、最近30天、最近3个月、自定义范围
- **AND** 系统 SHALL 实时更新所有图表和统计数据
- **AND** 系统 SHALL 记住用户的筛选偏好

#### Scenario: 按贡献者筛选
- **WHEN** 用户选择特定贡献者
- **THEN** 系统 SHALL 只显示该贡献者的提交数据
- **AND** 系统 SHALL 支持多选贡献者进行对比
- **AND** 系统 SHALL 提供贡献者搜索框

#### Scenario: 按提交类型筛选
- **WHEN** 用户勾选特定提交类型
- **THEN** 系统 SHALL 只显示选中类型的提交
- **AND** 系统 SHALL 支持多选类型组合筛选
- **AND** 筛选 SHALL 应用到所有图表和列表

#### Scenario: 搜索提交内容
- **WHEN** 用户在搜索框输入关键词
- **THEN** 系统 SHALL 搜索提交信息和文件名
- **AND** 系统 SHALL 高亮显示匹配的关键词
- **AND** 系统 SHALL 支持正则表达式搜索

### Requirement: 性能优化和缓存
系统 SHALL 优化查询性能，确保良好的用户体验。

#### Scenario: 大数据量快速加载
- **WHEN** 仓库有超过10000个提交记录
- **THEN** 系统 SHALL 在2秒内加载首屏数据
- **AND** 系统 SHALL 使用虚拟滚动加载提交列表
- **AND** 系统 SHALL 缓存常用查询结果

#### Scenario: 缓存统计数据
- **WHEN** 用户查看统计图表
- **THEN** 系统 SHALL 将聚合统计结果缓存到Redis
- **AND** 缓存 SHALL 设置1小时过期时间
- **AND** 新提交数据到达时 SHALL 自动刷新相关缓存

#### Scenario: 数据库查询优化
- **WHEN** 执行复杂的统计查询
- **THEN** 系统 SHALL 使用MySQL索引优化查询速度
- **AND** 系统 SHALL 使用预聚合表存储常用统计数据
- **AND** 系统 SHALL 避免全表扫描，限制查询结果集大小