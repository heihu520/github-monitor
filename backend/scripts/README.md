# 数据管理脚本

本目录包含数据库管理和数据同步相关的脚本工具。

## 脚本列表

### 1. clean_database.py - 数据库清理脚本

清空所有数据表，保留表结构。用于重新同步数据前的清理工作。

**使用方法：**

```bash
# 交互式清理（需要确认）
cd backend/scripts
python clean_database.py

# 自动确认清理（用于自动化脚本）
AUTO_CONFIRM=yes python clean_database.py
```

**功能：**
- 按照外键依赖顺序清空所有表
- 显示每个表删除的记录数
- 自动验证清理结果
- 保留表结构不变

**安全特性：**
- 默认需要用户确认
- 支持环境变量自动确认
- 事务保护，失败自动回滚

---

### 2. sync_github_data.py - GitHub数据同步脚本

从GitHub API同步用户、仓库和提交数据到数据库。支持完整同步和增量同步。

**使用方法：**

```bash
cd backend/scripts

# 增量同步（最近30天数据，每个仓库最多100个提交）
python sync_github_data.py <username>

# 完整同步（最近1年数据，所有提交）
python sync_github_data.py <username> --full

# 清空数据库后完整同步
python sync_github_data.py <username> --full --clean
```

**参数说明：**
- `username`: GitHub用户名（必需）
- `--full`: 完整同步模式
- `--clean`: 同步前清空数据库

**同步模式对比：**

| 模式 | 同步范围 | 提交限制 | 适用场景 |
|------|---------|---------|---------|
| 增量同步 | 最近30天 | 每仓库100个 | 日常更新 |
| 完整同步 | 最近1年 | 无限制 | 首次同步/重建数据 |

**同步流程：**
1. 同步用户基本信息
2. 同步仓库列表
3. 同步提交记录（按仓库）
4. 更新用户统计数据

**示例输出：**

```
============================================================
GitHub数据同步 - testuser
模式: 增量同步
============================================================

[1/3] 同步用户信息...
✅ 用户: testuser
   - 仓库数: 5
   - 提交数: 156

[2/3] 同步仓库列表...
✅ 同步了 5 个仓库

[3/3] 同步提交记录...
   模式: 增量同步（最近30天）

   [1/5] testuser/repo1
       ✓ 同步 25 个提交
   [2/5] testuser/repo2
       ○ 无新提交
   ...

[4/4] 更新用户统计...
✅ 统计数据已更新

============================================================
✅ 同步完成
------------------------------------------------------------
用户: testuser
仓库: 5 个
提交: 78 个
耗时: 45.23 秒
============================================================
```

---

## 使用场景

### 场景1：首次部署

```bash
# 1. 初始化数据库表（如果还没有）
cd backend
python init_db.py

# 2. 完整同步GitHub数据
cd scripts
python sync_github_data.py <your-username> --full
```

### 场景2：日常更新

```bash
# 增量同步最近变更
cd backend/scripts
python sync_github_data.py <your-username>
```

### 场景3：重建数据

```bash
# 清空后重新完整同步
cd backend/scripts
python sync_github_data.py <your-username> --full --clean
```

### 场景4：仅清空数据

```bash
# 只清空数据，不同步
cd backend/scripts
python clean_database.py
```

---

## 注意事项

1. **GitHub Token**：确保 `.env` 文件中配置了有效的 `GITHUB_TOKEN`

2. **速率限制**：
   - GitHub API 限制：5000次/小时（认证）
   - 完整同步可能消耗大量配额
   - 脚本会自动处理速率限制

3. **网络要求**：
   - 需要稳定的网络连接
   - 可能需要代理访问GitHub API
   - 同步大量数据时间较长

4. **数据库连接**：
   - 确保MySQL服务运行
   - 检查数据库连接配置
   - 足够的磁盘空间

5. **权限要求**：
   - 数据库用户需要 TRUNCATE 权限
   - GitHub Token 需要 repo 读取权限

---

## 故障排查

### 问题1：连接数据库失败

```bash
# 检查数据库服务
mysql -u hadoop -p

# 检查配置文件
cat backend/.env | grep DATABASE
```

### 问题2：GitHub API 速率限制

```bash
# 等待限制重置（通常1小时）
# 或使用 --full 参数降低请求频率
```

### 问题3：Unicode编码错误

脚本已自动处理Windows终端编码问题。如果仍有问题：

```bash
# Windows: 设置终端编码
chcp 65001

# 或使用环境变量
set PYTHONIOENCODING=utf-8
```

---

## 开发调试

### 启用调试日志

修改 `backend/app/core/config.py`：

```python
DEBUG = True  # 将显示所有SQL语句
```

### 手动测试单个组件

```python
# 测试GitHub客户端
python backend/test_github_client.py

# 测试数据同步服务
python backend/test_data_sync.py

# 测试仪表板服务
python backend/test_dashboard_service.py
```

---

## 相关文档

- [项目架构文档](../README.md)
- [数据库设计](../docs/database_schema.md)
- [API接口文档](../docs/api_reference.md)