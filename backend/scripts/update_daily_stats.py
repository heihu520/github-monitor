"""
更新每日统计数据
从commit_details聚合数据到daily_stats表
"""
import asyncio
import sys
from datetime import date, timedelta
from sqlalchemy import select, func, and_, text
from sqlalchemy.exc import IntegrityError

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models.commit_detail import CommitDetail
from app.models.daily_stat import DailyStat


async def update_daily_stats(user_id: int):
    """
    更新用户的每日统计数据
    
    Args:
        user_id: 用户ID
    """
    async with AsyncSessionLocal() as session:
        try:
            print(f"开始更新用户 {user_id} 的每日统计数据...")
            
            # 获取所有提交的日期范围
            result = await session.execute(
                text("""
                    SELECT 
                        MIN(DATE(commit_date)) as min_date,
                        MAX(DATE(commit_date)) as max_date
                    FROM commit_details
                    WHERE user_id = :user_id
                """),
                {"user_id": user_id}
            )
            
            date_range = result.first()
            if not date_range or not date_range.min_date:
                print(f"❌ 用户 {user_id} 没有提交数据")
                return
            
            min_date = date_range.min_date
            max_date = date_range.max_date
            
            print(f"日期范围: {min_date} 到 {max_date}")
            
            # 清空现有的daily_stats数据
            await session.execute(
                text("DELETE FROM daily_stats WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            
            # 按日期聚合提交数据
            result = await session.execute(
                text("""
                    SELECT
                        DATE(commit_date) as stat_date,
                        COUNT(*) as commits,
                        COALESCE(SUM(additions), 0) as additions,
                        COALESCE(SUM(deletions), 0) as deletions,
                        COUNT(DISTINCT repo_id) as active_repos
                    FROM commit_details
                    WHERE user_id = :user_id
                    GROUP BY DATE(commit_date)
                    ORDER BY stat_date
                """),
                {"user_id": user_id}
            )
            
            daily_data = result.all()
            
            # 插入每日统计数据
            insert_count = 0
            for row in daily_data:
                # 简单估算工作时长：每个提交约15分钟
                work_hours = round(row.commits * 0.25, 2)
                
                daily_stat = DailyStat(
                    user_id=user_id,
                    stat_date=row.stat_date,
                    commits=row.commits,
                    additions=row.additions,
                    deletions=row.deletions,
                    active_repos=row.active_repos,
                    work_hours=work_hours
                )
                
                session.add(daily_stat)
                insert_count += 1
            
            await session.commit()
            
            print(f"✅ 成功更新 {insert_count} 天的统计数据")
            print(f"   - 日期范围: {min_date} 到 {max_date}")
            print(f"   - 总天数: {insert_count}")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 更新失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='更新每日统计数据')
    parser.add_argument('user_id', type=int, help='用户ID')
    
    args = parser.parse_args()
    
    await update_daily_stats(args.user_id)


if __name__ == "__main__":
    asyncio.run(main())