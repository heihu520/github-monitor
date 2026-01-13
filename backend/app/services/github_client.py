"""
GitHub API客户端
封装GitHub REST API调用，处理认证、请求和响应
"""
import httpx
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

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
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化GitHub客户端
        
        Args:
            token: GitHub Personal Access Token，如果不提供则从配置读取
        """
        self.token = token or settings.GITHUB_TOKEN
        if not self.token:
            logger.warning("GitHub Token未配置，API请求将受限（60次/小时）")
        
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
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送HTTP请求到GitHub API
        
        Args:
            method: HTTP方法（GET, POST等）
            endpoint: API端点（如 /user/repos）
            params: URL查询参数
            json_data: JSON请求体
            
        Returns:
            响应JSON数据
            
        Raises:
            RateLimitError: 速率限制超限
            AuthenticationError: 认证失败
            GitHubAPIError: 其他API错误
        """
        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json_data
            )
            
            # 记录速率限制信息
            self._log_rate_limit(response.headers)
            
            # 处理错误响应
            if response.status_code == 401:
                raise AuthenticationError("GitHub Token无效或已过期")
            
            if response.status_code == 403:
                if "rate limit" in response.text.lower():
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
            logger.error(f"HTTP请求错误: {e}")
            raise GitHubAPIError(f"网络请求失败: {str(e)}")
    
    def _log_rate_limit(self, headers: Dict[str, str]) -> None:
        """
        记录API速率限制信息
        
        Args:
            headers: HTTP响应头
        """
        remaining = headers.get("X-RateLimit-Remaining")
        limit = headers.get("X-RateLimit-Limit")
        reset_timestamp = headers.get("X-RateLimit-Reset")
        
        if remaining and limit:
            logger.debug(f"API配额: {remaining}/{limit} 剩余")
            
            if reset_timestamp:
                reset_time = datetime.fromtimestamp(int(reset_timestamp))
                logger.debug(f"配额重置时间: {reset_time}")
            
            # 警告：配额即将用尽
            if int(remaining) < 100:
                logger.warning(f"⚠️  API配额不足: {remaining}/{limit}")
    
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
    
    async def close(self):
        """关闭HTTP客户端连接"""
        await self.client.aclose()
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()