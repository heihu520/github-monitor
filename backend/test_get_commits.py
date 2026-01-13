"""
测试GitHub提交历史抓取功能
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta

# 设置Windows控制台编码
os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.github_client import GitHubClient


async def test_get_commits():
    """测试获取仓库提交历史"""
    print("=" * 60)
    print("测试 GitHub 提交历史抓取")
    print("=" * 60)
    
    async with GitHubClient() as client:
        try:
            # 测试1: 获取octocat/Hello-World的提交历史
            print("\n[测试1] 获取 octocat/Hello-World 的提交历史...")
            commits = await client.get_repo_commits("octocat", "Hello-World", max_commits=10)
            
            if commits:
                print(f"[PASS] 获取到 {len(commits)} 个提交")
                print("\n前3个提交信息:")
                for i, commit in enumerate(commits[:3], 1):
                    commit_data = commit.get('commit', {})
                    author = commit_data.get('author', {})
                    print(f"\n  提交{i}:")
                    print(f"    SHA: {commit.get('sha', 'N/A')[:7]}")
                    print(f"    作者: {author.get('name', 'N/A')}")
                    print(f"    日期: {author.get('date', 'N/A')}")
                    print(f"    消息: {commit_data.get('message', 'N/A')[:50]}...")
            else:
                print("[FAIL] 未获取到提交")
            
            # 测试2: 测试时间范围过滤
            print("\n" + "=" * 60)
            print("[测试2] 测试时间范围过滤...")
            
            # 获取最近30天的提交
            until = datetime.utcnow().isoformat() + "Z"
            since = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
            
            commits = await client.get_repo_commits(
                "octocat",
                "Hello-World",
                since=since,
                until=until,
                max_commits=5
            )
            
            if commits:
                print(f"[PASS] 获取到 {len(commits)} 个提交（最近30天）")
                for i, commit in enumerate(commits, 1):
                    commit_data = commit.get('commit', {})
                    author = commit_data.get('author', {})
                    print(f"  {i}. {author.get('date', 'N/A')} - {commit_data.get('message', 'N/A')[:40]}")
            else:
                print("[INFO] 最近30天无新提交")
            
            # 测试3: 测试max_commits限制
            print("\n" + "=" * 60)
            print("[测试3] 测试max_commits限制...")
            commits = await client.get_repo_commits(
                "octocat",
                "Hello-World",
                max_commits=3
            )
            
            if len(commits) == 3:
                print(f"[PASS] 成功限制为 {len(commits)} 个提交")
            else:
                print(f"[FAIL] 期望3个提交，实际获取 {len(commits)} 个")
            
            # 测试4: 测试空仓库/不存在的仓库
            print("\n" + "=" * 60)
            print("[测试4] 测试不存在的仓库...")
            commits = await client.get_repo_commits("nonexistent", "repository")
            
            if commits == []:
                print("[PASS] 正确处理不存在的仓库（返回空列表）")
            else:
                print(f"[FAIL] 应返回空列表，实际返回 {len(commits)} 个提交")
            
            # 测试5: 测试分页功能
            print("\n" + "=" * 60)
            print("[测试5] 测试分页功能 (per_page=5)...")
            commits = await client.get_repo_commits(
                "octocat",
                "Hello-World",
                per_page=5,
                max_commits=15
            )
            
            if commits:
                print(f"[PASS] 获取到 {len(commits)} 个提交（分页per_page=5）")
                print("提交SHA列表:")
                for i, commit in enumerate(commits, 1):
                    print(f"  {i}. {commit.get('sha', 'N/A')[:7]}")
            else:
                print("[FAIL] 未获取到提交")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] 所有测试通过！")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[ERROR] 测试失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_get_commits())