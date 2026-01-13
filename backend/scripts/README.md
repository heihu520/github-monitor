# 数据库脚本使用指南

## 文件说明

- `init_database.sql` - MySQL数据库初始化SQL脚本
- `run_init_db.bat` - Windows批处理执行脚本

## 使用方法

### 方法一：使用批处理脚本（推荐）

1. 确保MySQL已安装并添加到PATH环境变量
2. 双击运行 `run_init_db.bat`
3. 按提示操作

### 方法二：手动执行SQL

1. 打开MySQL命令行客户端或使用MySQL Workbench
2. 确保连接到MySQL服务器（用户: hadoop, 密码: hadoop）
3. 执行以下命令：

```bash
# Windows CMD
mysql -u hadoop -phadoop github_monitor < init_database.sql

# PowerShell
Get-Content init_database.sql | mysql -u hadoop -phadoop github_monitor

# MySQL Workbench
# 打开 init_database.sql 文件并执行
```

### 方法三：使用Python脚本（即将实现）

```bash
cd backend
python scripts/init_db.py
```

## 数据库结构

### 表清单

1. **users** - 用户信息表
2. **repositories** - 仓库信息表
3. **daily_stats** - 每日统计数据表
4. **commit_details** - 提交详细信息表
5. **language_stats** - 编程语言统计表
6. **milestone_achievements** - 里程碑成就表
7. **coding_goals** - 编码目标表

### 表关系

```
users (1) ----< (N) repositories
users (1) ----< (N) daily_stats
users (1) ----< (N) commit_details
users (1) ----< (N) language_stats
users (1) ----< (N) milestone_achievements
users (1) ----< (N) coding_goals

repositories (1) ----< (N) commit_details
```

## 注意事项

⚠️ **警告**: 此脚本会删除所有现有表并重建，请谨慎使用！

- 首次部署：直接运行即可
- 已有数据：请先备份数据库
- 生产环境：不建议使用此脚本，应使用迁移工具

## 故障排查

### 问题1: 'mysql' 不是内部或外部命令

**原因**: MySQL未添加到PATH环境变量

**解决方案**:
1. 找到MySQL安装目录（如 `C:\Program Files\MySQL\MySQL Server 8.0\bin`）
2. 将该路径添加到系统PATH环境变量
3. 重启命令行窗口

### 问题2: Access denied for user 'hadoop'

**原因**: 用户名或密码错误，或用户权限不足

**解决方案**:
```sql
-- 以root用户登录MySQL
CREATE USER IF NOT EXISTS 'hadoop'@'localhost' IDENTIFIED BY 'hadoop';
GRANT ALL PRIVILEGES ON github_monitor.* TO 'hadoop'@'localhost';
FLUSH PRIVILEGES;
```

### 问题3: Unknown database 'github_monitor'

**原因**: 数据库不存在

**解决方案**:
```sql
-- 以root用户登录MySQL
CREATE DATABASE IF NOT EXISTS github_monitor 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;
```

## 下一步

数据库初始化完成后，请执行以下操作：

1. 验证表结构：
```sql
USE github_monitor;
SHOW TABLES;
DESCRIBE users;
```

2. 配置后端环境变量（backend/.env）
3. 运行后端应用测试数据库连接