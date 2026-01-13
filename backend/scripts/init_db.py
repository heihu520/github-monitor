"""
数据库初始化脚本 - 使用pymysql执行SQL文件
使用方法: python init_db.py
"""
import pymysql
import os
from pathlib import Path

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'hadoop',
    'password': 'hadoop',
    'database': 'github_monitor',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def read_sql_file(file_path: str) -> str:
    """读取SQL文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def execute_sql_file(connection, sql_content: str):
    """执行SQL文件内容"""
    # 分割SQL语句（按分号分隔）
    statements = []
    current_statement = []
    
    for line in sql_content.split('\n'):
        # 跳过注释行
        line = line.strip()
        if line.startswith('--') or line.startswith('/*') or line.startswith('*') or not line:
            continue
            
        current_statement.append(line)
        
        # 如果行以分号结束，表示一条完整SQL语句
        if line.endswith(';'):
            statement = ' '.join(current_statement)
            if statement.strip():
                statements.append(statement)
            current_statement = []
    
    # 执行所有SQL语句
    with connection.cursor() as cursor:
        for i, statement in enumerate(statements, 1):
            try:
                print(f"执行语句 {i}/{len(statements)}...")
                cursor.execute(statement)
                connection.commit()
            except Exception as e:
                print(f"错误: 语句 {i} 执行失败")
                print(f"SQL: {statement[:100]}...")
                print(f"错误信息: {e}")
                raise

def init_database():
    """初始化数据库"""
    print("=" * 60)
    print("GitHub Monitor 数据库初始化")
    print("=" * 60)
    print()
    print("数据库配置:")
    print(f"  主机: {DB_CONFIG['host']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print()
    print("警告: 此操作将删除所有现有表并重建！")
    print()
    
    # 确认操作
    confirm = input("确认继续？(yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("操作已取消")
        return
    
    print()
    print("开始执行...")
    print()
    
    # 获取SQL文件路径
    script_dir = Path(__file__).parent
    sql_file = script_dir / 'init_database.sql'
    
    if not sql_file.exists():
        print(f"错误: SQL文件不存在 - {sql_file}")
        return
    
    try:
        # 读取SQL文件
        print(f"读取SQL文件: {sql_file}")
        sql_content = read_sql_file(sql_file)
        
        # 连接数据库
        print(f"连接数据库: {DB_CONFIG['database']}")
        connection = pymysql.connect(**DB_CONFIG)
        
        try:
            # 执行SQL
            print("执行SQL语句...")
            execute_sql_file(connection, sql_content)
            
            # 验证表创建
            print()
            print("验证表结构...")
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                print()
                print("=" * 60)
                print("数据库初始化成功！")
                print("=" * 60)
                print()
                print(f"创建的表数量: {len(tables)}")
                print()
                print("表列表:")
                for table in tables:
                    table_name = list(table.values())[0]
                    print(f"  ✓ {table_name}")
                
        finally:
            connection.close()
            
    except pymysql.Error as e:
        print()
        print("=" * 60)
        print("数据库初始化失败！")
        print("=" * 60)
        print()
        print(f"错误代码: {e.args[0]}")
        print(f"错误信息: {e.args[1]}")
        print()
        print("可能的原因:")
        print("1. MySQL服务未启动")
        print("2. 用户名或密码错误")
        print("3. 数据库不存在")
        print("4. 权限不足")
        print()
        print("解决方案:")
        print("1. 确保MySQL服务正在运行")
        print("2. 检查backend/.env配置文件")
        print("3. 使用root用户创建数据库:")
        print("   CREATE DATABASE IF NOT EXISTS github_monitor")
        print("   CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("4. 授予hadoop用户权限:")
        print("   GRANT ALL PRIVILEGES ON github_monitor.* TO 'hadoop'@'localhost';")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("发生未知错误！")
        print("=" * 60)
        print()
        print(f"错误信息: {e}")

if __name__ == '__main__':
    init_database()