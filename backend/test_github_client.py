"""
GitHub客户端测试脚本
验证GitHubClient基本功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.services.github_client import GitHubClient, GitHubAPIError
from app.core.config import settings


async def test_github_client():
    """测试GitHub客户端基本功能"""
    print("=" * 60)
    print("GitHub客户端测试")
    print("=" * 60)
    print()
    
    # 检查Token配置
    if not settings.GITHUB_TOKEN:
        print("[ERROR] GitHub Token未配置")
        print("请在backend/.env文件中设置GITHUB_TOKEN")
        return False
    
    print(f"[INFO] GitHub Token: {settings.GITHUB_TOKEN[:10]}...")
    print()
    
    async with GitHubClient() as client:
        try:
            # 测试1: 获取速率限制
            print("测试 1: 获取API速率限制")
            print("-" * 60)
            rate_limit = await client.get_rate_limit()
            core = rate_limit.get("resources", {}).get("core", {})
            print(f"[PASS] API配额: {core.get('remaining')}/{core.get('limit')}")
            print(f"       重置时间: {core.get('reset')}")
            print()
            
            # 测试2: 获取用户信息
            print("测试 2: 获取用户信息")
            print("-" * 60)
            # 使用一个公开的GitHub用户名作为测试
            test_username = "octocat"  # GitHub的吉祥物账号
            user_info = await client.get_user(test_username)
            print(f"[PASS] 用户名: {user_info.get('login')}")
            print(f"       名称: {user_info.get('name')}")
            print(f"       公开仓库: {user_info.get('public_repos')}")
            print(f"       粉丝数: {user_info.get('followers')}")
            print()
            
            # 测试3: 错误处理 - 不存在的用户
            print("测试 3: 错误处理（不存在的用户）")
            print("-" * 60)
            try:
                await client.get_user("this-user-definitely-does-not-exist-12345")
                print("[FAIL] 应该抛出异常")
                return False
            except GitHubAPIError as e:
                print(f"[PASS] 正确捕获错误: {str(e)[:50]}...")
            print()
            
            print("=" * 60)
            print("[SUCCESS] 所有测试通过！")
            print("=" * 60)
            return True
            
        except Exception as e:
            print()
            print("=" * 60)
            print("[FAIL] 测试失败")
            print("=" * 60)
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = asyncio.run(test_github_client())
    sys.exit(0 if success else 1)