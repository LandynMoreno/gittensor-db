"""
Domain models for GitTensor database operations.
These mirror your gittensor.classes but are self-contained.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Repository:
    name: str
    owner: str
    
    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"

@dataclass 
class FileChange:
    filename: str
    changes: int
    additions: int
    deletions: int
    status: str
    patch: Optional[str] = None
    file_extension: Optional[str] = None
    
    def _calculate_file_extension(self) -> str:
        if '.' in self.filename:
            return self.filename.split('.')[-1]
        return ''

@dataclass
class PRDiff:
    pr_number: int
    repository_full_name: str
    files: List[FileChange]
    earned_score: float = 0.0

@dataclass
class PullRequest:
    number: int
    title: str
    repository: Repository
    merged_at: datetime
    created_at: datetime
    additions: int
    deletions: int
    commits: int
    author_login: str
    merged_by_login: Optional[str] = None
    
    @property
    def repository_full_name(self) -> str:
        return self.repository.full_name

@dataclass
class MinerEvaluation:
    uid: int
    github_id: Optional[str] = None
    failed_reason: Optional[str] = None
    total_score: float = 0.0
    total_lines_changed: int = 0
    total_open_prs: int = 0
    total_prs: int = 0
    unique_repos_contributed_to: Optional[List[str]] = None
    github_pat: Optional[str] = None