"""
更新用户统计数据脚本
从commit_details表聚合数据更新users表
"""
import sys
import os
from datetime import datetime, timedelta
import asyncio

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import AsyncSessionLocal
from sqlalchemy import text


async def calculate_streak_days(user_id: int, session) -> int:
    """计算连续编码天数"""
    # 获取最近的提交日期列表
    result = await session.execute(
        text("""
            SELECT DISTINCT DATE(commit_date) as commit_day
            FROM commit_details
            WHERE user_id = :user_id
            ORDER BY commit_day DESC
            LIMIT 365
        """),
        {"user_id": user_id}
    )
    
    dates = [row[0] for row in result.fetchall()]
    if not dates:
        return 0
    
    # 检查今天是否有提交
    today = datetime.now().date()
    if dates[0] != today and dates[0] != today - timedelta(days=1):
        return 0
    
    # 计算连续天数
    streak = 1
    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i + 1]).days
        if diff == 1:
            streak += 1
        else:
            break
    
    return streak


async def update_user_statistics(user_id: int):
    """更新指定用户的统计数据"""
    async with AsyncSessionLocal() as session:
        try:
            # 1. 从commit_details聚合数据
            stats_result = await session.execute(
                text("""
                    SELECT
                        COUNT(*) as total_commits,
                        COALESCE(SUM(additions), 0) as total_additions,
                        COALESCE(SUM(deletions), 0) as total_deletions,
                        COUNT(DISTINCT repo_id) as total_repos
                    FROM commit_details
                    WHERE user_id = :user_id
                """),
                {"user_id": user_id}
            )
            
            row = stats_result.fetchone()
            total_commits = row[0] or 0
            total_additions = row[1] or 0
            total_deletions = row[2] or 0
            total_repos = row[3] or 0
            
            # 2. 计算最活跃语言
            lang_result = await session.execute(
                text("""
                    SELECT primary_language, COUNT(*) as cnt
                    FROM commit_details
                    WHERE user_id = :user_id AND primary_language IS NOT NULL
                    GROUP BY primary_language
                    ORDER BY cnt DESC
                    LIMIT 1
                """),
                {"user_id": user_id}
            )
            
            lang_row = lang_result.fetchone()
            active_language = lang_row[0] if lang_row else 'Unknown'
            
            # 3. 计算连续天数
            streak_days = await calculate_streak_days(user_id, session)
            
            # 4. 计算最大连续天数（暂时等于当前连续天数）
            max_streak_days = streak_days
            
            # 5. 更新users表
            await session.execute(
                text("""
                    UPDATE users SET
                        total_commits = :total_commits,
                        total_additions = :total_additions,
                        total_deletions = :total_deletions,
                        total_repos = :total_repos,
                        streak_days = :streak_days,
                        max_streak_days = :max_streak_days,
                        active_language = :active_language,
                        updated_at = NOW()
                    WHERE id = :user_id
                """),
                {
                    "total_commits": total_commits,
                    "total_additions": total_additions,
                    "total_deletions": total_deletions,
                    "total_repos": total_repos,
                    "streak_days": streak_days,
                    "max_streak_days": max_streak_days,
                    "active_language": active_language,
                    "user_id": user_id
                }
            )
            
            await session.commit()
            
            print(f"✅ 用户 {user_id} 统计数据更新成功:")
            print(f"  - 总提交数: {total_commits}")
            print(f"  - 总新增行数: {total_additions}")
            print(f"  - 总删除行数: {total_deletions}")
            print(f"  - 总仓库数: {total_repos}")
            print(f"  - 连续天数: {streak_days}")
            print(f"  - 最活跃语言: {active_language}")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 更新用户统计失败: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: python update_user_stats.py <user_id>")
        sys.exit(1)
    
    user_id = int(sys.argv[1])
    
    print(f"开始更新用户 {user_id} 的统计数据...")
    asyncio.run(update_user_statistics(user_id))
    print("完成！")