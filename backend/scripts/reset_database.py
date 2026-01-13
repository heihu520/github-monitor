"""
完全重置数据库
清空所有表并重置自增ID
"""
import asyncio
import sys
from sqlalchemy import text

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal


async def reset_database():
    """完全重置数据库"""
    async with AsyncSessionLocal() as session:
        try:
            print("=" * 60)
            print("数据库完全重置")
            print("=" * 60)
            
            # 禁用外键检查
            await session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # 清空所有表
            tables = [
                'daily_stats',
                'language_stats',
                'coding_goals',
                'milestones',
                'commit_details',
                'repositories',
                'users'
            ]
            
            print("\n正在清空表...")
            for table in tables:
                try:
                    await session.execute(text(f"TRUNCATE TABLE {table}"))
                    print(f"  ✓ {table}")
                except Exception as e:
                    print(f"  ✗ {table}: {e}")
            
            # 重置自增ID
            print("\n正在重置自增ID...")
            for table in tables:
                try:
                    await session.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
                    print(f"  ✓ {table}")
                except Exception as e:
                    print(f"  ✗ {table}: {e}")
            
            # 启用外键检查
            await session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            await session.commit()
            
            print("\n" + "=" * 60)
            print("✅ 数据库重置完成")
            print("   - 所有表已清空")
            print("   - 自增ID已重置为1")
            print("=" * 60)
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ 重置失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """主函数"""
    print("\n⚠️  警告：此操作将删除所有数据并重置自增ID")
    print("是否继续？(yes/no): ", end="")
    
    if os.getenv('AUTO_CONFIRM') == 'yes':
        confirm = 'yes'
        print("yes (自动确认)")
    else:
        confirm = input().strip().lower()
    
    if confirm != 'yes':
        print("已取消操作")
        return
    
    await reset_database()


if __name__ == "__main__":
    asyncio.run(main())