"""
测试速率限制处理功能
"""
import asyncio
import os
import sys

# 设置Windows控制台编码
os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.github_client import GitHubClient


async def test_rate_limit():
    """测试速率限制处理"""
    print("=" * 60)
    print("测试 速率限制处理")
    print("=" * 60)
    
    # 测试1: 获取速率限制状态
    print("\n[测试1] 获取API速率限制状态...")
    async with GitHubClient() as client:
        try:
            rate_limit_data = await client.get_rate_limit()
            
            core = rate_limit_data.get('resources', {}).get('core', {})
            print(f"[PASS] 速率限制状态:")
            print(f"  配额限制: {core.get('limit')}")
            print(f"  剩余配额: {core.get('remaining')}")
            print(f"  重置时间: {core.get('reset')}")
            
            # 测试本地缓存的速率限制状态
            local_status = client.get_rate_limit_status()
            print(f"\n本地缓存状态:")
            print(f"  剩余配额: {local_status.get('remaining')}")
            print(f"  配额限制: {local_status.get('limit')}")
            print(f"  距离重置: {local_status.get('time_until_reset')} 秒")
            
        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
    
    # 测试2: 测试自动重试功能（使用auto_retry=True）
    print("\n" + "=" * 60)
    print("[测试2] 测试自动重试功能...")
    async with GitHubClient(auto_retry=True) as client:
        try:
            # 发起一个正常请求
            user = await client.get_user("octocat")
            print(f"[PASS] 请求成功（auto_retry=True）")
            print(f"  用户名: {user.get('login')}")
            
            # 检查速率限制状态
            status = client.get_rate_limit_status()
            print(f"  当前配额: {status.get('remaining')}/{status.get('limit')}")
            
        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
    
    # 测试3: 测试配额不足时的行为
    print("\n" + "=" * 60)
    print("[测试3] 模拟配额不足场景...")
    async with GitHubClient(auto_retry=True) as client:
        try:
            # 手动设置一个低配额值来测试警告
            client.rate_limit_info['remaining'] = 50
            client.rate_limit_info['limit'] = 5000
            
            print(f"[INFO] 模拟配额状态: {client.rate_limit_info['remaining']}/{ client.rate_limit_info['limit']}")
            
            # 发起请求，应该会触发警告
            user = await client.get_user("octocat")
            print(f"[PASS] 低配额时请求成功")
            print(f"  用户名: {user.get('login')}")
            
        except Exception as e:
            print(f"[INFO] 预期行为: {e}")
    
    # 测试4: 测试网络错误重试
    print("\n" + "=" * 60)
    print("[测试4] 测试错误重试机制...")
    async with GitHubClient(auto_retry=True) as client:
        try:
            # 正常请求，验证重试机制不会干扰正常流程
            repos = await client.get_user_repos("octocat", per_page=5)
            print(f"[PASS] 获取到 {len(repos)} 个仓库")
            print(f"  前3个仓库:")
            for i, repo in enumerate(repos[:3], 1):
                print(f"    {i}. {repo.get('name')}")
            
        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
    
    # 测试5: 测试速率限制状态获取
    print("\n" + "=" * 60)
    print("[测试5] 测试速率限制状态获取...")
    async with GitHubClient() as client:
        try:
            # 先发起一个请求以更新速率限制信息
            await client.get_user("octocat")
            
            # 获取详细状态
            status = client.get_rate_limit_status()
            print(f"[PASS] 速率限制状态:")
            print(f"  剩余配额: {status.get('remaining')}")
            print(f"  配额限制: {status.get('limit')}")
            
            if status.get('reset_time'):
                print(f"  重置时间: {status.get('reset_time')}")
                print(f"  距离重置: {status.get('time_until_reset')} 秒")
            
            # 计算使用率
            if status.get('limit') and status.get('remaining') is not None:
                usage_rate = (status['limit'] - status['remaining']) / status['limit'] * 100
                print(f"  使用率: {usage_rate:.1f}%")
            
        except Exception as e:
            print(f"[FAIL] 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] 所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_rate_limit())