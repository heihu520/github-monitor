"""
数据库清理脚本
清空所有表数据，保留表结构
用于重新同步数据前的清理工作
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
    """清空所有表数据"""
    print("=" * 60)
    print("数据库清理脚本")
    print("=" * 60)
    
    # 定义表清理顺序（按照外键依赖关系，先删除子表）
    tables = [
        'commit_details',      # 提交详情（依赖users和repositories）
        'daily_stats',         # 每日统计（依赖users）
        'language_stats',      # 语言统计（依赖users）
        'milestone_achievements',  # 里程碑成就（依赖users）
        'coding_goals',        # 编码目标（依赖users）
        'repositories',        # 仓库（依赖users）
        'users',              # 用户（基础表）
    ]
    
    async with AsyncSessionLocal() as db:
        try:
            print("\n开始清理数据...")
            print("-" * 60)
            
            # 禁用外键检查（MySQL）
            await db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            total_deleted = 0
            
            for table in tables:
                # 查询当前表记录数
                count_result = await db.execute(text(f"SELECT COUNT(*) as cnt FROM {table}"))
                count = count_result.scalar()
                
                if count > 0:
                    # 删除表数据
                    await db.execute(text(f"TRUNCATE TABLE {table}"))
                    print(f"✓ 清空表 {table:25s} - 删除 {count:6d} 条记录")
                    total_deleted += count
                else:
                    print(f"○ 跳过表 {table:25s} - 已为空")
            
            # 启用外键检查
            await db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            # 提交事务
            await db.commit()
            
            print("-" * 60)
            print(f"\n✅ 清理完成！共删除 {total_deleted} 条记录")
            print("\n所有表已清空，表结构保留完整")
            print("=" * 60)
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ 清理失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def verify_cleanup():
    """验证清理结果"""
    print("\n验证清理结果...")
    print("-" * 60)
    
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
        all_empty = True
        
        for table in tables:
            count_result = await db.execute(text(f"SELECT COUNT(*) as cnt FROM {table}"))
            count = count_result.scalar()
            
            status = "✓" if count == 0 else "✗"
            print(f"{status} 表 {table:25s}: {count} 条记录")
            
            if count > 0:
                all_empty = False
        
        print("-" * 60)
        
        if all_empty:
            print("✅ 验证通过：所有表已清空")
        else:
            print("⚠️  警告：部分表仍有数据")
        
        return all_empty


async def main():
    """主函数"""
    print("\n⚠️  警告：此操作将清空所有数据表！")
    print("请确认是否继续？(yes/no): ", end="")
    
    # 在自动化环境中，可以通过环境变量跳过确认
    if os.getenv('AUTO_CONFIRM') == 'yes':
        confirm = 'yes'
        print("yes (自动确认)")
    else:
        confirm = input().strip().lower()
    
    if confirm != 'yes':
        print("\n已取消清理操作")
        return
    
    try:
        # 执行清理
        await clean_all_tables()
        
        # 验证结果
        await verify_cleanup()
        
    except Exception as e:
        print(f"\n❌ 操作失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())