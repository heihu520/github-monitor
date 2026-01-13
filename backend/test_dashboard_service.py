"""
测试DashboardService数据库集成
验证从数据库查询和聚合数据的功能
"""
import asyncio
import sys
from datetime import datetime, date, timedelta
from sqlalchemy import select

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.core.database import AsyncSessionLocal
from app.services.dashboard_service import DashboardService
from app.models.user import User
from app.models.repository import Repository
from app.models.commit_detail import CommitDetail
from app.models.daily_stat import DailyStat


async def test_dashboard_service():
    """测试DashboardService"""
    print("=" * 60)
    print("测试 DashboardService 数据库集成")
    print("=" * 60)
    
    async with AsyncSessionLocal() as db:
        # 1. 查找测试用户
        print("\n[1] 查找用户...")
        result = await db.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ 数据库中没有用户数据")
            print("💡 请先运行 test_data_sync.py 同步数据")
            return
        
        print(f"✅ 找到用户: {user.username} (ID: {user.id})")
        print(f"   - 总仓库数: {user.total_repos}")
        print(f"   - 总提交数: {user.total_commits}")
        print(f"   - 连续天数: {user.streak_days}")
        print(f"   - 活跃语言: {user.active_language}")
        
        # 2. 创建DashboardService实例
        service = DashboardService(db)
        
        # 3. 测试统计数据
        print("\n[2] 测试统计数据...")
        stats = await service.get_dashboard_stats(user.id)
        print(f"✅ 统计数据获取成功:")
        print(f"   今日: {stats.today_commits} 提交, +{stats.today_additions}/-{stats.today_deletions} 行")
        print(f"   本周: {stats.week_commits} 提交, +{stats.week_additions}/-{stats.week_deletions} 行")
        print(f"   本月: {stats.month_commits} 提交, +{stats.month_additions}/-{stats.month_deletions} 行")
        print(f"   连续: {stats.streak_days} 天")
        print(f"   语言: {stats.active_language}")
        print(f"   工时: {stats.work_hours:.1f} 小时")
        print(f"   仓库: {stats.total_repositories}")
        print(f"   代码: {stats.code_lines} 行")
        
        # 4. 测试里程碑成就
        print("\n[3] 测试里程碑成就...")
        milestones = await service.get_milestones(user.id)
        print(f"✅ 获取到 {len(milestones)} 个里程碑:")
        
        achieved_count = sum(1 for m in milestones if m.achieved)
        print(f"   已达成: {achieved_count}/{len(milestones)}")
        
        for milestone in milestones:
            status = "✓" if milestone.achieved else " "
            print(f"   [{status}] {milestone.name}: {milestone.current_value}/{milestone.threshold} ({milestone.progress:.1f}%)")
        
        # 5. 测试趋势数据
        print("\n[4] 测试趋势数据 (最近7天)...")
        trend_data = await service.get_trend_data(user.id, days=7)
        print(f"✅ 获取到 {len(trend_data)} 天的趋势数据:")
        
        total_trend_commits = sum(t.commits for t in trend_data)
        print(f"   7天总提交: {total_trend_commits}")
        
        for i, trend in enumerate(trend_data[-3:], 1):  # 显示最后3天
            print(f"   Day {len(trend_data) - 3 + i}: {trend.date} - {trend.commits} 提交, +{trend.additions}/-{trend.deletions}")
        
        # 6. 测试热力图数据
        print("\n[5] 测试热力图数据 (最近30天)...")
        heatmap_data = await service.get_heatmap_data(user.id, days=30)
        print(f"✅ 获取到 {len(heatmap_data)} 天的热力图数据:")
        
        # 统计活跃度等级分布
        level_counts = {}
        for h in heatmap_data:
            level_counts[h.level] = level_counts.get(h.level, 0) + 1
        
        print(f"   活跃度分布:")
        for level in range(5):
            count = level_counts.get(level, 0)
            bar = "█" * (count // 2) if count > 0 else ""
            print(f"   Level {level}: {count:2d} 天 {bar}")
        
        # 7. 测试完整总览
        print("\n[6] 测试完整总览...")
        overview = await service.get_dashboard_overview(user.id)
        print(f"✅ 总览数据获取成功:")
        print(f"   统计数据: ✓")
        print(f"   里程碑: {len(overview.milestones)} 个")
        print(f"   趋势数据: {len(overview.trend_data)} 天")
        print(f"   热力图: {len(overview.heatmap_data)} 天")
        
        print("\n" + "=" * 60)
        print("✅ DashboardService 数据库集成测试完成")
        print("=" * 60)


async def check_data_status():
    """检查数据库数据状态"""
    print("\n[数据库状态检查]")
    print("-" * 60)
    
    async with AsyncSessionLocal() as db:
        # 检查用户
        user_count = await db.execute(select(User))
        users = user_count.scalars().all()
        print(f"用户数: {len(users)}")
        
        # 检查仓库
        repo_count = await db.execute(select(Repository))
        repos = repo_count.scalars().all()
        print(f"仓库数: {len(repos)}")
        
        # 检查提交
        commit_count = await db.execute(select(CommitDetail))
        commits = commit_count.scalars().all()
        print(f"提交数: {len(commits)}")
        
        # 检查每日统计
        daily_count = await db.execute(select(DailyStat))
        dailies = daily_count.scalars().all()
        print(f"每日统计: {len(dailies)}")
        
        if len(users) == 0:
            print("\n⚠️  数据库为空，请先运行:")
            print("   python test_data_sync.py")
        
        print("-" * 60)


async def main():
    """主函数"""
    try:
        await check_data_status()
        await test_dashboard_service()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())