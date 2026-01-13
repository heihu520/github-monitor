"""
修改用户ID
将用户ID从源ID修改为目标ID
"""
import asyncio
import sys
from sqlalchemy import text

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal


async def change_user_id(from_id: int, to_id: int):
    """
    修改用户ID
    
    Args:
        from_id: 源用户ID
        to_id: 目标用户ID
    """
    async with AsyncSessionLocal() as session:
        try:
            print(f"将用户ID从 {from_id} 修改为 {to_id}...")
            
            # 1. 检查目标ID是否已存在
            result = await session.execute(
                text("SELECT id FROM users WHERE id = :to_id"),
                {"to_id": to_id}
            )
            existing = result.first()
            
            if existing:
                print(f"⚠️  用户ID {to_id} 已存在，先删除...")
                
                # 删除关联数据
                await session.execute(
                    text("DELETE FROM daily_stats WHERE user_id = :to_id"),
                    {"to_id": to_id}
                )
                await session.execute(
                    text("DELETE FROM commit_details WHERE user_id = :to_id"),
                    {"to_id": to_id}
                )
                await session.execute(
                    text("DELETE FROM repositories WHERE user_id = :to_id"),
                    {"to_id": to_id}
                )
                await session.execute(
                    text("DELETE FROM users WHERE id = :to_id"),
                    {"to_id": to_id}
                )
                
                print(f"✅ 已删除用户ID {to_id} 的所有数据")
            
            # 2. 更新用户ID
            await session.execute(
                text("UPDATE users SET id = :to_id WHERE id = :from_id"),
                {"from_id": from_id, "to_id": to_id}
            )
            
            # 3. 更新关联表
            await session.execute(
                text("UPDATE repositories SET user_id = :to_id WHERE user_id = :from_id"),
                {"from_id": from_id, "to_id": to_id}
            )
            
            await session.execute(
                text("UPDATE commit_details SET user_id = :to_id WHERE user_id = :from_id"),
                {"from_id": from_id, "to_id": to_id}
            )
            
            await session.execute(
                text("UPDATE daily_stats SET user_id = :to_id WHERE user_id = :from_id"),
                {"from_id": from_id, "to_id": to_id}
            )
            
            await session.commit()
            
            print(f"✅ 用户ID修改成功: {from_id} → {to_id}")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 修改失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='修改用户ID')
    parser.add_argument('from_id', type=int, help='源用户ID')
    parser.add_argument('to_id', type=int, help='目标用户ID')
    
    args = parser.parse_args()
    
    print(f"⚠️  警告：此操作将修改用户ID及所有关联数据")
    print(f"源ID: {args.from_id}")
    print(f"目标ID: {args.to_id}")
    print()
    
    await change_user_id(args.from_id, args.to_id)


if __name__ == "__main__":
    asyncio.run(main())