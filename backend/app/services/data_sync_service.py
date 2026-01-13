"""
数据同步服务
从GitHub API获取数据并持久化到数据库
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.repository import Repository
from app.models.commit_detail import CommitDetail
from app.services.github_client import GitHubClient
from app.services.commit_parser import CommitParser

logger = logging.getLogger(__name__)


class DataSyncService:
    """数据同步服务类"""
    
    def __init__(self, db: AsyncSession, github_client: GitHubClient):
        """
        初始化数据同步服务
        
        Args:
            db: 数据库会话
            github_client: GitHub API客户端
        """
        self.db = db
        self.github_client = github_client
    
    async def sync_user(self, username: str) -> User:
        """
        同步用户信息
        
        Args:
            username: GitHub用户名
            
        Returns:
            用户ORM对象
        """
        # 检查用户是否已存在
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # 从GitHub获取用户信息
            github_user = await self.github_client.get_user(username)
            
            # 创建新用户
            user = User(
                username=username,
                email=github_user.get('email'),
                avatar_url=github_user.get('avatar_url')
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info(f"创建新用户: {username}")
        
        return user
    
    async def sync_repositories(self, user: User) -> List[Repository]:
        """
        同步用户的所有仓库
        
        Args:
            user: 用户ORM对象
            
        Returns:
            仓库ORM对象列表
        """
        # 从GitHub获取仓库列表
        github_repos = await self.github_client.get_user_repos(user.username)
        
        synced_repos = []
        
        for github_repo in github_repos:
            # 检查仓库是否已存在
            result = await self.db.execute(
                select(Repository).where(
                    Repository.user_id == user.id,
                    Repository.github_repo_id == github_repo['id']
                )
            )
            repo = result.scalar_one_or_none()
            
            if repo:
                # 更新现有仓库
                repo.repo_name = github_repo['full_name']
                repo.description = github_repo.get('description')
                repo.language = github_repo.get('language')
                repo.stars = github_repo.get('stargazers_count', 0)
                repo.forks = github_repo.get('forks_count', 0)
                repo.is_private = github_repo.get('private', False)
            else:
                # 创建新仓库
                repo = Repository(
                    user_id=user.id,
                    github_repo_id=github_repo['id'],
                    repo_name=github_repo['full_name'],
                    description=github_repo.get('description'),
                    language=github_repo.get('language'),
                    stars=github_repo.get('stargazers_count', 0),
                    forks=github_repo.get('forks_count', 0),
                    is_private=github_repo.get('private', False)
                )
                self.db.add(repo)
            
            synced_repos.append(repo)
        
        await self.db.commit()
        
        # 刷新所有仓库对象
        for repo in synced_repos:
            await self.db.refresh(repo)
        
        # 更新用户的仓库总数
        user.total_repos = len(synced_repos)
        await self.db.commit()
        
        logger.info(f"同步了 {len(synced_repos)} 个仓库 (用户: {user.username})")
        
        return synced_repos
    
    async def sync_commits(
        self,
        user: User,
        repository: Repository,
        since: Optional[str] = None,
        max_commits: Optional[int] = 100
    ) -> List[CommitDetail]:
        """
        同步仓库的提交记录
        
        Args:
            user: 用户ORM对象
            repository: 仓库ORM对象
            since: 起始时间（ISO 8601格式）
            max_commits: 最大同步提交数
            
        Returns:
            提交详情ORM对象列表
        """
        # 解析仓库名称
        parts = repository.repo_name.split('/')
        if len(parts) != 2:
            logger.error(f"无效的仓库名称: {repository.repo_name}")
            return []
        
        owner, repo_name = parts
        
        # 从GitHub获取提交历史
        github_commits = await self.github_client.get_repo_commits(
            owner,
            repo_name,
            since=since,
            max_commits=max_commits
        )
        
        if not github_commits:
            logger.info(f"仓库 {repository.repo_name} 没有新提交")
            return []
        
        synced_commits = []
        
        for github_commit in github_commits:
            commit_sha = github_commit.get('sha')
            
            # 检查提交是否已存在
            result = await self.db.execute(
                select(CommitDetail).where(CommitDetail.commit_sha == commit_sha)
            )
            existing_commit = result.scalar_one_or_none()
            
            if existing_commit:
                continue  # 跳过已存在的提交
            
            # 获取提交详情
            commit_detail = await self.github_client.get_commit_detail(
                owner,
                repo_name,
                commit_sha
            )
            
            # 解析提交信息
            parsed_commit = CommitParser.parse_commit(commit_detail)
            
            # 解析提交时间
            commit_date = datetime.fromisoformat(
                parsed_commit['commit_date'].replace('Z', '+00:00')
            )
            
            # 提取语言（使用第一个语言，如果有的话）
            primary_language = (
                parsed_commit['languages'][0] 
                if parsed_commit['languages'] 
                else repository.language
            )
            
            # 创建提交记录
            commit_obj = CommitDetail(
                user_id=user.id,
                repo_id=repository.id,
                commit_sha=commit_sha,
                commit_message=parsed_commit['message'],
                commit_date=commit_date,
                additions=parsed_commit['additions'],
                deletions=parsed_commit['deletions'],
                files_changed=parsed_commit['files_changed'],
                primary_language=primary_language,
                commit_hour=CommitParser.extract_commit_hour(parsed_commit['commit_date']),
                commit_weekday=commit_date.weekday()
            )
            
            self.db.add(commit_obj)
            synced_commits.append(commit_obj)
        
        if synced_commits:
            await self.db.commit()
            
            # 刷新所有提交对象
            for commit in synced_commits:
                await self.db.refresh(commit)
            
            # 更新仓库的最后提交时间
            if synced_commits:
                latest_commit = max(synced_commits, key=lambda c: c.commit_date)
                repository.last_commit_at = latest_commit.commit_date
            
            # 更新用户统计
            await self._update_user_stats(user)
            
            await self.db.commit()
        
        logger.info(f"同步了 {len(synced_commits)} 个新提交 (仓库: {repository.repo_name})")
        
        return synced_commits
    
    async def _update_user_stats(self, user: User) -> None:
        """
        更新用户的统计数据
        
        Args:
            user: 用户ORM对象
        """
        # 查询用户的所有提交
        result = await self.db.execute(
            select(CommitDetail).where(CommitDetail.user_id == user.id)
        )
        all_commits = result.scalars().all()
        
        if not all_commits:
            return
        
        # 统计数据
        user.total_commits = len(all_commits)
        user.total_additions = sum(c.additions for c in all_commits)
        user.total_deletions = sum(c.deletions for c in all_commits)
        
        # 统计最活跃语言
        language_count = {}
        for commit in all_commits:
            if commit.primary_language:
                language_count[commit.primary_language] = language_count.get(
                    commit.primary_language, 0
                ) + 1
        
        if language_count:
            user.active_language = max(language_count, key=language_count.get)
        
        logger.debug(f"更新用户统计: {user.username} - {user.total_commits} commits")
    
    async def sync_user_data(
        self,
        username: str,
        max_repos: Optional[int] = None,
        max_commits_per_repo: int = 100,
        incremental: bool = True
    ) -> Dict[str, Any]:
        """
        完整同步用户数据（用户、仓库、提交）
        
        Args:
            username: GitHub用户名
            max_repos: 最大同步仓库数（None表示全部）
            max_commits_per_repo: 每个仓库最大同步提交数
            incremental: 是否启用增量同步（默认True）
            
        Returns:
            同步结果统计
        """
        logger.info(f"开始同步用户数据: {username} (增量模式: {incremental})")
        
        # 1. 同步用户
        user = await self.sync_user(username)
        
        # 2. 确定同步起始时间
        since = None
        if incremental and user.last_sync_at:
            since = user.last_sync_at.isoformat()
            logger.info(f"增量同步，起始时间: {since}")
        else:
            logger.info("全量同步")
        
        # 3. 同步仓库
        repos = await self.sync_repositories(user)
        
        if max_repos:
            repos = repos[:max_repos]
        
        # 4. 同步提交
        total_commits = 0
        for repo in repos:
            commits = await self.sync_commits(
                user,
                repo,
                since=since,
                max_commits=max_commits_per_repo
            )
            total_commits += len(commits)
        
        # 5. 更新最后同步时间
        user.last_sync_at = datetime.utcnow()
        await self.db.commit()
        
        result = {
            'username': username,
            'user_id': user.id,
            'total_repos_synced': len(repos),
            'total_commits_synced': total_commits,
            'total_additions': user.total_additions,
            'total_deletions': user.total_deletions,
            'sync_mode': 'incremental' if (incremental and since) else 'full',
            'since': since
        }
        
        logger.info(f"完成用户数据同步: {result}")
        
        return result