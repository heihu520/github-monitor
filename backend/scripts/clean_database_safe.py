"""
安全的数据库清理脚本
使用DELETE而非TRUNCATE，避免锁表问题
"""
import asyncio
import sys
from sqlalchemy import text

# 添加项目根目录到路径
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.core.database import AsyncSessionLocal


async def clean_all_tables():
    """使用DELETE清空所有表数据"""
    print("=" * 60)
    print("安全数据库清理脚本 (使用DELETE)")
    print("=" * 60)
    
    # 定义表清理顺序（按照外键依赖关系）
    tables = [
        'commit_details',
        'daily_stats',
        'language_stats',
        'milestone_achievements',
        'coding_goals',
        'repositories',
        'users',
    ]
    
    async with AsyncSessionLocal() as db:
        try:
            print("\n开始清理数据...")
            print("-" * 60)
            
            total_deleted = 0
            
            for table in tables:
                # 查询当前表记录数
                count_result = await db.execute(text(f"SELECT COUNT(*) as cnt FROM {table}"))
                count = count_result.scalar()
                
                if count > 0:
                    # 使用DELETE删除数据
                    await db.execute(text(f"DELETE FROM {table}"))
                    print(f"✓ 清空表 {table:25s} - 删除 {count:6d} 条记录")
                    total_deleted += count
                else:
                    print(f"○ 跳过表 {table:25s} - 已为空")
            
            # 提交事务
            await db.commit()
            
            print("-" * 60)
            print(f"\n✅ 清理完成！共删除 {total_deleted} 条记录")
            print("=" * 60)
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ 清理失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """主函数"""
    print("\n⚠️  警告：此操作将清空所有数据表！")
    print("请确认是否继续？(yes/no): ", end="")
    
    if os.getenv('AUTO_CONFIRM') == 'yes':
        confirm = 'yes'
        print("yes (自动确认)")
    else:
        confirm = input().strip().lower()
    
    if confirm != 'yes':
        print("\n已取消清理操作")
        return
    
    try:
        await clean_all_tables()
    except Exception as e:
        print(f"\n❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())