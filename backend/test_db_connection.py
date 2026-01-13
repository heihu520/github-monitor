"""
数据库连接测试脚本
验证数据库配置和连接是否正常
"""
import asyncio
import sys
import os
from pathlib import Path

# 设置Windows控制台编码为UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import check_db_health, AsyncSessionLocal, engine
from app.models import User
from sqlalchemy import select, text


async def test_basic_connection():
    """测试基本数据库连接"""
    print("=" * 60)
    print("测试 1: 基本数据库连接")
    print("=" * 60)
    
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            print("[PASS] 数据库连接成功")
            print(f"   查询结果: {result.scalar()}")
            return True
    except Exception as e:
        print(f"[FAIL] 数据库连接失败: {e}")
        return False


async def test_health_check():
    """测试健康检查函数"""
    print("\n" + "=" * 60)
    print("测试 2: 数据库健康检查")
    print("=" * 60)
    
    is_healthy = await check_db_health()
    if is_healthy:
        print("[PASS] 健康检查通过")
    else:
        print("[FAIL] 健康检查失败")
    return is_healthy


async def test_table_exists():
    """测试表是否存在"""
    print("\n" + "=" * 60)
    print("测试 3: 检查数据库表")
    print("=" * 60)
    
    try:
        async with AsyncSessionLocal() as session:
            # 查询所有表
            result = await session.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            print(f"[PASS] 找到 {len(tables)} 个表:")
            for table in tables:
                print(f"   - {table}")
            
            # 检查核心表
            required_tables = [
                'users', 'repositories', 'daily_stats',
                'commit_details', 'language_stats',
                'milestone_achievements', 'coding_goals'
            ]
            
            missing = [t for t in required_tables if t not in tables]
            if missing:
                print(f"\n[WARN] 缺少以下表: {', '.join(missing)}")
                print("   请运行: cd backend/scripts && python init_db.py")
                return False
            else:
                print(f"\n[PASS] 所有核心表都存在")
                return True
                
    except Exception as e:
        print(f"[FAIL] 检查表失败: {e}")
        return False


async def test_orm_query():
    """测试ORM模型查询"""
    print("\n" + "=" * 60)
    print("测试 4: ORM模型查询")
    print("=" * 60)
    
    try:
        async with AsyncSessionLocal() as session:
            # 查询用户表
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            print(f"[PASS] ORM查询成功")
            print(f"   用户数量: {len(users)}")
            
            if users:
                print("\n   用户列表:")
                for user in users:
                    print(f"   - ID: {user.id}, 用户名: {user.username}, 提交数: {user.total_commits}")
            else:
                print("   [NOTE] 数据库为空，可以开始添加数据")
            
            return True
            
    except Exception as e:
        print(f"[FAIL] ORM查询失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False


async def test_crud_operations():
    """测试CRUD操作"""
    print("\n" + "=" * 60)
    print("测试 5: CRUD操作（创建测试用户）")
    print("=" * 60)
    
    try:
        async with AsyncSessionLocal() as session:
            # 创建测试用户
            test_user = User(
                username="test_user_temp",
                email="test@example.com",
                total_commits=0,
                streak_days=0
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print(f"[PASS] 创建用户成功")
            print(f"   ID: {test_user.id}")
            print(f"   用户名: {test_user.username}")
            
            # 删除测试用户
            await session.delete(test_user)
            await session.commit()
            
            print(f"[PASS] 删除用户成功")
            print(f"   CRUD操作测试通过")
            
            return True
            
    except Exception as e:
        print(f"[FAIL] CRUD操作失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("\n>> 开始数据库连接测试\n")
    
    results = []
    
    # 执行所有测试
    results.append(("基本连接", await test_basic_connection()))
    results.append(("健康检查", await test_health_check()))
    results.append(("表结构", await test_table_exists()))
    results.append(("ORM查询", await test_orm_query()))
    results.append(("CRUD操作", await test_crud_operations()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{name:15} {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n[SUCCESS] 所有测试通过！数据库配置正确。")
    else:
        print("\n[WARNING] 部分测试失败，请检查配置和数据库状态。")
    
    # 关闭连接
    await engine.dispose()
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)