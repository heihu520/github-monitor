"""
测试数据库清理脚本
验证脚本逻辑是否正确
"""
import asyncio
import sys

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy import text
from app.core.database import AsyncSessionLocal


async def test_verify_cleanup():
    """测试验证清理功能"""
    print("=" * 60)
    print("测试清理验证功能")
    print("=" * 60)
    
    tables = [
        'users',
        'repositories',
        'commit_details',
        'daily_stats',
        'language_stats',
        'milestone_achievements',
        'coding_goals'
    ]
    
    async with AsyncSessionLocal() as db:
        print("\n当前数据库状态:")
        print("-" * 60)
        
        total_records = 0
        
        for table in tables:
            try:
                count_result = await db.execute(text(f"SELECT COUNT(*) as cnt FROM {table}"))
                count = count_result.scalar()
                
                status = "✓" if count == 0 else "○"
                print(f"{status} 表 {table:25s}: {count:6d} 条记录")
                
                total_records += count
            except Exception as e:
                print(f"✗ 表 {table:25s}: 错误 - {e}")
        
        print("-" * 60)
        print(f"总计: {total_records} 条记录")
        print("=" * 60)
        
        if total_records == 0:
            print("✅ 数据库已为空")
        else:
            print(f"ℹ️  数据库包含 {total_records} 条记录")
            print("\n可以运行以下命令清理:")
            print("  cd backend/scripts")
            print("  AUTO_CONFIRM=yes python clean_database.py")


async def main():
    """主函数"""
    try:
        await test_verify_cleanup()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())