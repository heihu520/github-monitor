"""
提交详情解析器
解析GitHub提交数据，提取统计信息
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class CommitParser:
    """提交详情解析器"""
    
    # 常见编程语言文件扩展名映射
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.vue': 'Vue',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.xml': 'XML',
    }
    
    @staticmethod
    def parse_commit(commit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析单个提交的详细信息
        
        Args:
            commit_data: GitHub API返回的提交详情
            
        Returns:
            解析后的提交信息字典，包含:
            - sha: 提交哈希
            - message: 提交消息
            - author_name: 作者名称
            - author_email: 作者邮箱
            - commit_date: 提交时间
            - files_changed: 变更文件数
            - additions: 新增行数
            - deletions: 删除行数
            - total_changes: 总变更行数
            - languages: 涉及的编程语言列表
            - file_types: 文件类型统计
        """
        commit_info = commit_data.get('commit', {})
        author_info = commit_info.get('author', {})
        stats = commit_data.get('stats', {})
        files = commit_data.get('files', [])
        
        # 基本信息
        parsed = {
            'sha': commit_data.get('sha', ''),
            'message': commit_info.get('message', ''),
            'author_name': author_info.get('name', ''),
            'author_email': author_info.get('email', ''),
            'commit_date': author_info.get('date', ''),
        }
        
        # 统计信息
        parsed.update({
            'files_changed': len(files),
            'additions': stats.get('additions', 0),
            'deletions': stats.get('deletions', 0),
            'total_changes': stats.get('total', 0),
        })
        
        # 解析文件语言和类型
        languages = set()
        file_types = {}
        
        for file_info in files:
            filename = file_info.get('filename', '')
            
            # 提取文件扩展名
            ext = CommitParser._get_file_extension(filename)
            if ext:
                # 统计文件类型
                file_types[ext] = file_types.get(ext, 0) + 1
                
                # 识别编程语言
                language = CommitParser.LANGUAGE_EXTENSIONS.get(ext)
                if language:
                    languages.add(language)
        
        parsed['languages'] = list(languages)
        parsed['file_types'] = file_types
        
        return parsed
    
    @staticmethod
    def parse_commit_batch(commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量解析提交列表
        
        Args:
            commits: 提交列表
            
        Returns:
            解析后的提交信息列表
        """
        return [CommitParser.parse_commit(commit) for commit in commits]
    
    @staticmethod
    def _get_file_extension(filename: str) -> Optional[str]:
        """
        获取文件扩展名
        
        Args:
            filename: 文件名
            
        Returns:
            扩展名（包含点），如果没有则返回None
        """
        if '.' not in filename:
            return None
        
        # 处理多重扩展名（如 .spec.ts）
        parts = filename.split('/')[-1].split('.')
        if len(parts) >= 2:
            return '.' + parts[-1]
        
        return None
    
    @staticmethod
    def aggregate_stats(parsed_commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        聚合多个提交的统计信息
        
        Args:
            parsed_commits: 解析后的提交列表
            
        Returns:
            聚合统计信息，包含:
            - total_commits: 总提交数
            - total_additions: 总新增行数
            - total_deletions: 总删除行数
            - total_changes: 总变更行数
            - total_files: 总变更文件数
            - languages: 所有涉及的语言及次数
            - file_types: 所有文件类型及次数
            - top_contributors: 贡献者排名
        """
        if not parsed_commits:
            return {
                'total_commits': 0,
                'total_additions': 0,
                'total_deletions': 0,
                'total_changes': 0,
                'total_files': 0,
                'languages': {},
                'file_types': {},
                'top_contributors': []
            }
        
        stats = {
            'total_commits': len(parsed_commits),
            'total_additions': 0,
            'total_deletions': 0,
            'total_changes': 0,
            'total_files': 0,
        }
        
        languages_count = {}
        file_types_count = {}
        contributors = {}
        
        for commit in parsed_commits:
            # 累加统计
            stats['total_additions'] += commit.get('additions', 0)
            stats['total_deletions'] += commit.get('deletions', 0)
            stats['total_changes'] += commit.get('total_changes', 0)
            stats['total_files'] += commit.get('files_changed', 0)
            
            # 语言统计
            for lang in commit.get('languages', []):
                languages_count[lang] = languages_count.get(lang, 0) + 1
            
            # 文件类型统计
            for ext, count in commit.get('file_types', {}).items():
                file_types_count[ext] = file_types_count.get(ext, 0) + count
            
            # 贡献者统计
            author = commit.get('author_name', 'Unknown')
            if author not in contributors:
                contributors[author] = {
                    'name': author,
                    'email': commit.get('author_email', ''),
                    'commits': 0,
                    'additions': 0,
                    'deletions': 0
                }
            contributors[author]['commits'] += 1
            contributors[author]['additions'] += commit.get('additions', 0)
            contributors[author]['deletions'] += commit.get('deletions', 0)
        
        stats['languages'] = languages_count
        stats['file_types'] = file_types_count
        
        # 按提交数排序贡献者
        stats['top_contributors'] = sorted(
            contributors.values(),
            key=lambda x: x['commits'],
            reverse=True
        )
        
        return stats
    
    @staticmethod
    def extract_commit_hour(commit_date: str) -> int:
        """
        提取提交时间的小时数（用于活动时间分析）
        
        Args:
            commit_date: ISO 8601格式的时间字符串
            
        Returns:
            小时数 (0-23)
        """
        try:
            dt = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
            return dt.hour
        except Exception:
            return 0
    
    @staticmethod
    def categorize_commit_message(message: str) -> str:
        """
        根据提交消息分类提交类型
        
        Args:
            message: 提交消息
            
        Returns:
            提交类型 (feat/fix/docs/refactor/test/other)
        """
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ['feat', 'feature', 'add', 'new']):
            return 'feat'
        elif any(keyword in message_lower for keyword in ['fix', 'bug', 'patch']):
            return 'fix'
        elif any(keyword in message_lower for keyword in ['doc', 'readme', 'comment']):
            return 'docs'
        elif any(keyword in message_lower for keyword in ['refactor', 'clean', 'improve']):
            return 'refactor'
        elif any(keyword in message_lower for keyword in ['test', 'spec']):
            return 'test'
        else:
            return 'other'