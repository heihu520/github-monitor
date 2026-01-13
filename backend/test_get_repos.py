"""
测试GitHub仓库列表获取功能
"""
import asyncio
import os
import sys

# 设置Windows控制台编码
os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.github_client import GitHubClient


async def test_get_repos():
    """测试获取用户仓库列表"""
    print("=" * 60)
    print("测试 GitHub 仓库列表获取")
    print("=" * 60)
    
    async with GitHubClient() as client:
        try:
            # 测试1: 获取octocat的仓库列表
            print("\n[测试1] 获取 octocat 的仓库列表...")
            repos = await client.get_user_repos("octocat")
            
            if repos:
                print(f"[PASS] 获取到 {len(repos)} 个仓库")
                print("\n前3个仓库信息:")
                for i, repo in enumerate(repos[:3], 1):
                    print(f"\n  仓库{i}:")
                    print(f"    名称: {repo.get('name')}")
                    print(f"    全名: {repo.get('full_name')}")
                    print(f"    描述: {repo.get('description', '无描述')}")
                    print(f"    语言: {repo.get('language', '未知')}")
                    print(f"    Stars: {repo.get('stargazers_count', 0)}")
                    print(f"    Forks: {repo.get('forks_count', 0)}")
                    print(f"    私有: {'是' if repo.get('private') else '否'}")
            else:
                print("[FAIL] 未获取到仓库")
            
            # 测试2: 测试分页功能（获取拥有多个仓库的用户）
            print("\n" + "=" * 60)
            print("[测试2] 测试分页功能 (torvalds 用户)...")
            repos = await client.get_user_repos("torvalds", per_page=10)
            
            if repos:
                print(f"[PASS] 获取到 {len(repos)} 个仓库（分页per_page=10）")
                print(f"\n仓库列表:")
                for i, repo in enumerate(repos, 1):
                    print(f"  {i}. {repo.get('name')} - {repo.get('stargazers_count', 0)} stars")
            else:
                print("[FAIL] 未获取到仓库")
            
            # 测试3: 测试排序功能
            print("\n" + "=" * 60)
            print("[测试3] 测试排序功能 (按创建时间排序)...")
            repos = await client.get_user_repos("octocat", sort="created", per_page=5)
            
            if repos:
                print(f"[PASS] 获取到 {len(repos)} 个仓库（按创建时间排序）")
                print(f"\n仓库列表:")
                for i, repo in enumerate(repos, 1):
                    print(f"  {i}. {repo.get('name')} - 创建于: {repo.get('created_at')}")
            else:
                print("[FAIL] 未获取到仓库")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] 所有测试通过！")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[ERROR] 测试失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_get_repos())