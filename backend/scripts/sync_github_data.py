"""
GitHub数据同步脚本
支持完整同步和增量同步
"""
import asyncio
import sys
from datetime import datetime, timedelta

# 添加项目根目录到路径
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.services.github_client import GitHubClient
from app.services.data_sync_service import DataSyncService


async def sync_user_data(username: str, full_sync: bool = False):
    """
    同步用户数据
    
    Args:
        username: GitHub用户名
        full_sync: 是否完整同步（True=同步所有历史，False=只同步最近数据）
    """
    print("=" * 60)
    print(f"GitHub数据同步 - {username}")
    print(f"模式: {'完整同步' if full_sync else '增量同步'}")
    print("=" * 60)
    
    # 创建客户端和服务
    github_client = GitHubClient(settings.GITHUB_TOKEN)
    
    async with AsyncSessionLocal() as db:
        sync_service = DataSyncService(db, github_client)
        
        try:
            start_time = datetime.now()
            
            # 1. 同步用户基本信息
            print("\n[1/3] 同步用户信息...")
            user = await sync_service.sync_user(username)
            print(f"✅ 用户: {user.username}")
            print(f"   - 仓库数: {user.total_repos}")
            print(f"   - 提交数: {user.total_commits}")
            
            # 2. 同步仓库列表
            print("\n[2/3] 同步仓库列表...")
            repos = await sync_service.sync_user_repositories(user.id, username)
            print(f"✅ 同步了 {len(repos)} 个仓库")
            
            # 3. 同步提交记录
            print("\n[3/3] 同步提交记录...")
            
            if full_sync:
                print("   模式: 完整同步（所有历史提交）")
                max_commits_per_repo = None  # 不限制
                days_back = 365  # 1年内的提交
            else:
                print("   模式: 增量同步（最近30天）")
                max_commits_per_repo = 100  # 每个仓库最多100个
                days_back = 30
            
            since_date = datetime.now() - timedelta(days=days_back)
            
            total_commits = 0
            for i, repo in enumerate(repos, 1):
                print(f"\n   [{i}/{len(repos)}] {repo.repo_name}")
                
                try:
                    commits = await sync_service.sync_repository_commits(
                        user_id=user.id,
                        repo_id=repo.id,
                        repo_full_name=repo.repo_name,
                        since=since_date,
                        max_commits=max_commits_per_repo
                    )
                    
                    if commits:
                        print(f"       ✓ 同步 {len(commits)} 个提交")
                        total_commits += len(commits)
                    else:
                        print(f"       ○ 无新提交")
                        
                except Exception as e:
                    print(f"       ✗ 错误: {e}")
                    continue
            
            # 4. 更新用户统计
            print("\n[4/4] 更新用户统计...")
            await sync_service.update_user_stats(user.id)
            print("✅ 统计数据已更新")
            
            # 提交所有更改
            await db.commit()
            
            # 统计结果
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("\n" + "=" * 60)
            print("✅ 同步完成")
            print("-" * 60)
            print(f"用户: {username}")
            print(f"仓库: {len(repos)} 个")
            print(f"提交: {total_commits} 个")
            print(f"耗时: {duration:.2f} 秒")
            print("=" * 60)
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ 同步失败: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub数据同步脚本')
    parser.add_argument('username', help='GitHub用户名')
    parser.add_argument(
        '--full',
        action='store_true',
        help='完整同步（同步所有历史数据）'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='同步前清空数据库'
    )
    
    args = parser.parse_args()
    
    # 如果需要清空数据库
    if args.clean:
        print("\n⚠️  将在同步前清空数据库")
        print("是否继续？(yes/no): ", end="")
        
        if os.getenv('AUTO_CONFIRM') == 'yes':
            confirm = 'yes'
            print("yes (自动确认)")
        else:
            confirm = input().strip().lower()
        
        if confirm != 'yes':
            print("已取消操作")
            return
        
        # 导入并执行清理脚本
        from clean_database import clean_all_tables
        await clean_all_tables()
        print()
    
    # 执行同步
    await sync_user_data(args.username, full_sync=args.full)


if __name__ == "__main__":
    asyncio.run(main())