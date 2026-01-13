@echo off
REM =====================================================
REM GitHub Monitor 数据库初始化批处理脚本
REM 使用方法: 双击运行或在命令行执行 run_init_db.bat
REM =====================================================

echo ========================================
echo GitHub Monitor 数据库初始化
echo ========================================
echo.
echo 数据库信息:
echo - 用户名: hadoop
echo - 密码: hadoop
echo - 数据库: github_monitor
echo.
echo 警告: 此操作将删除所有现有表并重建！
echo.
pause

echo.
echo 正在执行数据库初始化...
echo.

REM 设置MySQL路径（根据实际安装路径调整）
set MYSQL_PATH=mysql

REM 执行SQL脚本
%MYSQL_PATH% -u hadoop -phadoop github_monitor < init_database.sql

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 数据库初始化成功！
    echo ========================================
) else (
    echo.
    echo ========================================
    echo 数据库初始化失败！
    echo 错误代码: %errorlevel%
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. MySQL未安装或未添加到PATH环境变量
    echo 2. 用户名或密码错误
    echo 3. 数据库不存在
    echo 4. SQL脚本语法错误
    echo.
    echo 请检查以上问题后重试
)

echo.
pause