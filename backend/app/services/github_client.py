"""
GitHub API客户端
封装GitHub REST API调用，处理认证、请求和响应
"""
import httpx
import logging
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)


class GitHubAPIError(Exception):
    """GitHub API错误基类"""
    pass


class RateLimitError(GitHubAPIError):
    """速率限制错误"""
    pass


class AuthenticationError(GitHubAPIError):
    """认证错误"""
    pass


class GitHubClient:
    """
    GitHub API客户端
    
    使用示例:
        client = GitHubClient(token="ghp_xxx")
        repos = await client.get_user_repos("username")
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, auto_retry: bool = True):
        """
        初始化GitHub客户端
        
        Args:
            token: GitHub Personal Access Token，如果不提供则从配置读取
            auto_retry: 是否在遇到速率限制时自动重试
        """
        self.token = token or settings.GITHUB_TOKEN
        if not self.token:
            logger.warning("GitHub Token未配置，API请求将受限（60次/小时）")
        
        self.auto_retry = auto_retry
        self.rate_limit_info = {
            'remaining': None,
            'limit': None,
            'reset': None
        }
        
        # 配置HTTP客户端
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Monitor-App",
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        
        # 创建异步HTTP客户端
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True
        )
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        发送HTTP请求到GitHub API（支持自动重试）
        
        Args:
            method: HTTP方法（GET, POST等）
            endpoint: API端点（如 /user/repos）
            params: URL查询参数
            json_data: JSON请求体
            max_retries: 最大重试次数
            
        Returns:
            响应JSON数据
            
        Raises:
            RateLimitError: 速率限制超限且未启用自动重试
            AuthenticationError: 认证失败
            GitHubAPIError: 其他API错误
        """
        retries = 0
        
        while retries <= max_retries:
            try:
                # 检查是否需要等待速率限制重置
                if self.auto_retry:
                    await self._check_rate_limit()
                
                response = await self.client.request(
                    method=method,
                    url=endpoint,
                    params=params,
                    json=json_data
                )
                
                # 更新速率限制信息
                self._update_rate_limit(response.headers)
                
                # 处理错误响应
                if response.status_code == 401:
                    raise AuthenticationError("GitHub Token无效或已过期")
                
                if response.status_code == 403:
                    if "rate limit" in response.text.lower():
                        if self.auto_retry and retries < max_retries:
                            wait_time = self._calculate_wait_time()
                            logger.warning(f"遇到速率限制，等待 {wait_time} 秒后重试...")
                            await asyncio.sleep(wait_time)
                            retries += 1
                            continue
                        raise RateLimitError("API速率限制已达上限")
                    raise GitHubAPIError(f"访问被拒绝: {response.text}")
                
                if response.status_code == 404:
                    raise GitHubAPIError(f"资源不存在: {endpoint}")
                
                if response.status_code >= 400:
                    raise GitHubAPIError(
                        f"API请求失败 (状态码: {response.status_code}): {response.text}"
                    )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPError as e:
                if retries < max_retries:
                    logger.warning(f"HTTP请求错误，重试中... ({retries + 1}/{max_retries})")
                    retries += 1
                    await asyncio.sleep(2 ** retries)  # 指数退避
                    continue
                logger.error(f"HTTP请求错误: {e}")
                raise GitHubAPIError(f"网络请求失败: {str(e)}")
        
        raise GitHubAPIError(f"请求失败，已达最大重试次数 ({max_retries})")
    
    def _update_rate_limit(self, headers: Dict[str, str]) -> None:
        """
        更新速率限制信息
        
        Args:
            headers: HTTP响应头
        """
        remaining = headers.get("X-RateLimit-Remaining")
        limit = headers.get("X-RateLimit-Limit")
        reset_timestamp = headers.get("X-RateLimit-Reset")
        
        if remaining and limit:
            self.rate_limit_info['remaining'] = int(remaining)
            self.rate_limit_info['limit'] = int(limit)
            
            if reset_timestamp:
                self.rate_limit_info['reset'] = int(reset_timestamp)
                reset_time = datetime.fromtimestamp(int(reset_timestamp))
                logger.debug(f"配额重置时间: {reset_time}")
            
            logger.debug(f"API配额: {remaining}/{limit} 剩余")
            
            # 警告：配额即将用尽
            if int(remaining) < 100:
                logger.warning(f"⚠️  API配额不足: {remaining}/{limit}")
    
    async def _check_rate_limit(self) -> None:
        """
        检查速率限制，如果配额不足则等待
        """
        if self.rate_limit_info['remaining'] is not None:
            if self.rate_limit_info['remaining'] < 10:  # 剩余配额低于10
                wait_time = self._calculate_wait_time()
                if wait_time > 0:
                    logger.warning(f"API配额不足，等待 {wait_time} 秒...")
                    await asyncio.sleep(wait_time)
    
    def _calculate_wait_time(self) -> int:
        """
        计算需要等待的时间（秒）
        
        Returns:
            等待时间（秒）
        """
        if self.rate_limit_info['reset'] is None:
            return 60  # 默认等待60秒
        
        now = datetime.now().timestamp()
        reset_time = self.rate_limit_info['reset']
        
        wait_time = max(0, int(reset_time - now) + 5)  # 额外等待5秒确保配额已重置
        return wait_time
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        获取当前速率限制状态（本地缓存）
        
        Returns:
            速率限制状态字典
        """
        status = self.rate_limit_info.copy()
        
        if status['reset']:
            status['reset_time'] = datetime.fromtimestamp(status['reset']).isoformat()
            status['time_until_reset'] = max(0, int(status['reset'] - datetime.now().timestamp()))
        
        return status
    
    async def get_rate_limit(self) -> Dict[str, Any]:
        """
        获取当前速率限制状态
        
        Returns:
            速率限制信息
        """
        return await self._request("GET", "/rate_limit")
    
    async def get_user(self, username: str) -> Dict[str, Any]:
        """
        获取用户信息
        
        Args:
            username: GitHub用户名
            
        Returns:
            用户信息字典
        """
        return await self._request("GET", f"/users/{username}")
    
    async def get_user_repos(
        self,
        username: str,
        type: str = "all",
        sort: str = "updated",
        per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """
        获取用户的所有仓库列表
        
        Args:
            username: GitHub用户名
            type: 仓库类型 (all, owner, member) 默认all
            sort: 排序方式 (created, updated, pushed, full_name) 默认updated
            per_page: 每页数量，最大100
            
        Returns:
            仓库列表
        """
        repos = []
        page = 1
        
        while True:
            params = {
                "type": type,
                "sort": sort,
                "per_page": per_page,
                "page": page
            }
            
            batch = await self._request("GET", f"/users/{username}/repos", params=params)
            
            if not batch:
                break
            
            repos.extend(batch)
            
            # 如果返回数量小于per_page，说明已经是最后一页
            if len(batch) < per_page:
                break
            
            page += 1
        
        logger.info(f"获取到 {len(repos)} 个仓库 (用户: {username})")
        return repos
    
    async def get_repo_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        per_page: int = 100,
        max_commits: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        获取仓库的提交历史
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            since: 起始时间 (ISO 8601格式, 例如: 2024-01-01T00:00:00Z)
            until: 结束时间 (ISO 8601格式)
            per_page: 每页数量，最大100
            max_commits: 最大获取提交数量，None表示获取所有
            
        Returns:
            提交列表
        """
        commits = []
        page = 1
        
        while True:
            params = {
                "per_page": per_page,
                "page": page
            }
            
            if since:
                params["since"] = since
            if until:
                params["until"] = until
            
            try:
                batch = await self._request(
                    "GET",
                    f"/repos/{owner}/{repo}/commits",
                    params=params
                )
            except GitHubAPIError as e:
                # 如果仓库为空或无提交，返回空列表
                if "资源不存在" in str(e) or "404" in str(e):
                    logger.warning(f"仓库 {owner}/{repo} 无提交或不存在")
                    return []
                raise
            
            if not batch:
                break
            
            commits.extend(batch)
            
            # 如果设置了最大提交数，检查是否已达到
            if max_commits and len(commits) >= max_commits:
                commits = commits[:max_commits]
                break
            
            # 如果返回数量小于per_page，说明已经是最后一页
            if len(batch) < per_page:
                break
            
            page += 1
        
        logger.info(f"获取到 {len(commits)} 个提交 (仓库: {owner}/{repo})")
        return commits
    
    async def get_commit_detail(
        self,
        owner: str,
        repo: str,
        sha: str
    ) -> Dict[str, Any]:
        """
        获取单个提交的详细信息
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            sha: 提交SHA
            
        Returns:
            提交详细信息，包含文件变更、统计数据等
        """
        return await self._request("GET", f"/repos/{owner}/{repo}/commits/{sha}")
    
    async def close(self):
        """关闭HTTP客户端连接"""
        await self.client.aclose()
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()