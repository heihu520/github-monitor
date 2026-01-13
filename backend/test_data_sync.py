"""
测试数据持久化服务
"""
import asyncio
import os
import sys

# 设置Windows控制台编码
os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db, AsyncSessionLocal
from app.services.github_client import GitHubClient
from app.services.data_sync_service import DataSyncService
from app.models.user import User
from app.models.repository import Repository
from app.models.commit_detail import CommitDetail
from sqlalchemy import select


async def test_data_sync():
    """测试数据同步服务"""
    print("=" * 60)
    print("测试 数据持久化服务")
    print("=" * 60)
    
    # 创建数据库会话
    async with AsyncSessionLocal() as db:
        try:
            # 创建GitHub客户端
            github_client = GitHubClient()
            
            # 创建数据同步服务
            sync_service = DataSyncService(db, github_client)
            
            # 测试1: 同步用户信息
            print("\n[测试1] 同步用户信息...")
            test_username = "octocat"
            user = await sync_service.sync_user(test_username)
            
            print(f"[PASS] 用户同步成功")
            print(f"  用户ID: {user.id}")
            print(f"  用户名: {user.username}")
            print(f"  邮箱: {user.email or '未设置'}")
            print(f"  头像: {user.avatar_url[:50] if user.avatar_url else '无'}...")
            
            # 测试2: 同步仓库列表
            print("\n" + "=" * 60)
            print("[测试2] 同步仓库列表...")
            repos = await sync_service.sync_repositories(user)
            
            print(f"[PASS] 同步了 {len(repos)} 个仓库")
            print(f"\n前5个仓库:")
            for i, repo in enumerate(repos[:5], 1):
                print(f"  {i}. {repo.repo_name}")
                print(f"     语言: {repo.language or '未知'}")
                print(f"     Stars: {repo.stars}")
                print(f"     描述: {(repo.description[:40] + '...') if repo.description else '无'}")
            
            # 测试3: 同步提交记录（只同步第一个仓库）
            print("\n" + "=" * 60)
            print("[测试3] 同步提交记录...")
            if repos:
                test_repo = repos[0]
                print(f"  同步仓库: {test_repo.repo_name}")
                
                commits = await sync_service.sync_commits(
                    user,
                    test_repo,
                    max_commits=5
                )
                
                print(f"[PASS] 同步了 {len(commits)} 个新提交")
                
                if commits:
                    print(f"\n提交详情:")
                    for i, commit in enumerate(commits[:3], 1):
                        print(f"  {i}. SHA: {commit.commit_sha[:7]}")
                        print(f"     消息: {commit.commit_message[:50]}...")
                        print(f"     变更: +{commit.additions} -{commit.deletions}")
                        print(f"     语言: {commit.primary_language or '未知'}")
                        print(f"     时间: {commit.commit_date}")
            
            # 测试4: 查询数据库验证数据已保存
            print("\n" + "=" * 60)
            print("[测试4] 验证数据库中的数据...")
            
            # 查询用户
            result = await db.execute(
                select(User).where(User.username == test_username)
            )
            db_user = result.scalar_one_or_none()
            
            if db_user:
                print(f"[PASS] 用户数据已保存")
                print(f"  总仓库数: {db_user.total_repos}")
                print(f"  总提交数: {db_user.total_commits}")
                print(f"  总新增行: {db_user.total_additions}")
                print(f"  总删除行: {db_user.total_deletions}")
                print(f"  活跃语言: {db_user.active_language or '未设置'}")
                
                # 查询仓库数量
                result = await db.execute(
                    select(Repository).where(Repository.user_id == db_user.id)
                )
                db_repos = result.scalars().all()
                print(f"\n  数据库中的仓库数: {len(db_repos)}")
                
                # 查询提交数量
                result = await db.execute(
                    select(CommitDetail).where(CommitDetail.user_id == db_user.id)
                )
                db_commits = result.scalars().all()
                print(f"  数据库中的提交数: {len(db_commits)}")
            else:
                print("[FAIL] 用户数据未找到")
            
            # 测试5: 完整同步（小规模）
            print("\n" + "=" * 60)
            print("[测试5] 测试完整同步功能...")
            
            sync_result = await sync_service.sync_user_data(
                test_username,
                max_repos=3,  # 只同步前3个仓库
                max_commits_per_repo=5  # 每个仓库只同步5个提交
            )
            
            print(f"[PASS] 完整同步完成")
            print(f"  用户: {sync_result['username']}")
            print(f"  同步仓库数: {sync_result['total_repos_synced']}")
            print(f"  同步提交数: {sync_result['total_commits_synced']}")
            print(f"  总新增行: {sync_result['total_additions']}")
            print(f"  总删除行: {sync_result['total_deletions']}")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] 所有测试通过！")
            print("=" * 60)
            
            # 关闭GitHub客户端
            await github_client.close()
            
        except Exception as e:
            print(f"\n[ERROR] 测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 关闭数据库会话
            await db.close()


if __name__ == "__main__":
    asyncio.run(test_data_sync())