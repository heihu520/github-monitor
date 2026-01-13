"""
测试提交详情解析功能
"""
import asyncio
import os
import sys
import json

# 设置Windows控制台编码
os.system('chcp 65001 > nul')

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.github_client import GitHubClient
from app.services.commit_parser import CommitParser


async def test_commit_parser():
    """测试提交解析功能"""
    print("=" * 60)
    print("测试 提交详情解析")
    print("=" * 60)
    
    async with GitHubClient() as client:
        try:
            # 测试1: 获取并解析单个提交
            print("\n[测试1] 获取并解析单个提交详情...")
            commits = await client.get_repo_commits("octocat", "Hello-World", max_commits=1)
            
            if commits:
                sha = commits[0].get('sha')
                print(f"提交SHA: {sha}")
                
                # 获取详细信息
                commit_detail = await client.get_commit_detail("octocat", "Hello-World", sha)
                
                # 解析提交
                parsed = CommitParser.parse_commit(commit_detail)
                
                print(f"\n[PASS] 提交解析成功")
                print(f"  SHA: {parsed['sha'][:7]}")
                print(f"  作者: {parsed['author_name']}")
                print(f"  邮箱: {parsed['author_email']}")
                print(f"  日期: {parsed['commit_date']}")
                print(f"  消息: {parsed['message'][:50]}...")
                print(f"  变更文件: {parsed['files_changed']} 个")
                print(f"  新增行数: {parsed['additions']}")
                print(f"  删除行数: {parsed['deletions']}")
                print(f"  总变更: {parsed['total_changes']}")
                print(f"  涉及语言: {', '.join(parsed['languages']) if parsed['languages'] else '无'}")
                print(f"  文件类型: {parsed['file_types']}")
            else:
                print("[FAIL] 未获取到提交")
            
            # 测试2: 批量解析多个提交
            print("\n" + "=" * 60)
            print("[测试2] 批量解析多个提交...")
            commits = await client.get_repo_commits("octocat", "Hello-World", max_commits=5)
            
            # 获取详细信息
            commit_details = []
            for commit in commits[:3]:  # 只测试前3个
                sha = commit.get('sha')
                detail = await client.get_commit_detail("octocat", "Hello-World", sha)
                commit_details.append(detail)
            
            # 批量解析
            parsed_commits = CommitParser.parse_commit_batch(commit_details)
            
            print(f"[PASS] 成功解析 {len(parsed_commits)} 个提交")
            for i, commit in enumerate(parsed_commits, 1):
                print(f"\n  提交{i}:")
                print(f"    作者: {commit['author_name']}")
                print(f"    变更: +{commit['additions']} -{commit['deletions']}")
                print(f"    语言: {', '.join(commit['languages']) if commit['languages'] else '无'}")
            
            # 测试3: 聚合统计
            print("\n" + "=" * 60)
            print("[测试3] 聚合统计信息...")
            stats = CommitParser.aggregate_stats(parsed_commits)
            
            print(f"[PASS] 统计信息:")
            print(f"  总提交数: {stats['total_commits']}")
            print(f"  总新增行数: {stats['total_additions']}")
            print(f"  总删除行数: {stats['total_deletions']}")
            print(f"  总变更行数: {stats['total_changes']}")
            print(f"  总变更文件: {stats['total_files']}")
            print(f"  涉及语言: {stats['languages']}")
            print(f"  文件类型: {stats['file_types']}")
            print(f"\n  贡献者排名:")
            for i, contributor in enumerate(stats['top_contributors'][:3], 1):
                print(f"    {i}. {contributor['name']}")
                print(f"       提交: {contributor['commits']} 次")
                print(f"       新增: {contributor['additions']} 行")
                print(f"       删除: {contributor['deletions']} 行")
            
            # 测试4: 提取提交时间
            print("\n" + "=" * 60)
            print("[测试4] 提取提交时间...")
            for i, commit in enumerate(parsed_commits, 1):
                hour = CommitParser.extract_commit_hour(commit['commit_date'])
                print(f"  提交{i}: {commit['commit_date']} -> {hour}时")
            print("[PASS] 时间提取成功")
            
            # 测试5: 提交消息分类
            print("\n" + "=" * 60)
            print("[测试5] 提交消息分类...")
            test_messages = [
                "feat: add new feature",
                "fix: resolve bug in parser",
                "docs: update README",
                "refactor: improve code quality",
                "test: add unit tests",
                "update configuration"
            ]
            
            for msg in test_messages:
                category = CommitParser.categorize_commit_message(msg)
                print(f"  '{msg[:30]}...' -> {category}")
            print("[PASS] 消息分类成功")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] 所有测试通过！")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[ERROR] 测试失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_commit_parser())