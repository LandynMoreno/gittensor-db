"""
Domain models for GitTensor database operations.
These mirror your gittensor.classes but are self-contained.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Set, Callable
from datetime import datetime
from ..utils.utils import parse_github_timestamp

GITHUB_DOMAIN = 'https://github.com/'

@dataclass
class Repository:
    """Repository information"""
    name: str
    owner: str
    
    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.name}"
    
    def construct_github_url(self) -> str:
        return GITHUB_DOMAIN + self.full_name

@dataclass
class FileChange:
    """Represents a single file change in a PR diff"""
    filename: str
    changes: int
    additions: int
    deletions: int
    status: str  # "added", "modified", "removed", etc.
    patch: Optional[str] = None  # The actual diff content
    file_extension: Optional[str] = None
    
    def __post_init__(self):
        if self.file_extension is None:
            self.file_extension = self._calculate_file_extension()
    
    def _calculate_file_extension(self) -> str:
        return self.filename.split(".")[-1].lower() if "." in self.filename else ""

@dataclass
class PRDiff:
    """Represents the complete diff details and earned score for a pull request"""
    pr_number: int
    repository_full_name: str
    files: List[FileChange]
    earned_score: float = 0.0
    
    @property
    def total_changes(self) -> int:
        """Total changes across all files"""
        return sum(file.changes for file in self.files)
    
    @property
    def file_types(self) -> set:
        """Set of all file extensions in this diff"""
        return {file.file_extension for file in self.files if file.file_extension}
    
    def construct_github_url(self) -> str:
        return GITHUB_DOMAIN + f"{self.repository_full_name}/pull/{self.pr_number}/files"
    
    @classmethod
    def from_github_response(cls, pr_number: int, repo_full_name: str, files_data: List[dict]) -> 'PRDiff':
        """Create PRDiff from GitHub API files response"""
        files = []
        for file_data in files_data:
            file_change = FileChange(
                filename=file_data['filename'],
                changes=file_data['changes'],
                additions=file_data['additions'],
                deletions=file_data['deletions'],
                status=file_data['status'],
                patch=file_data.get('patch')
            )
            files.append(file_change)
        
        return cls(
            pr_number=pr_number,
            repository_full_name=repo_full_name,
            files=files
        )

@dataclass
class Issue:
    """Represents an issue that belongs to a pull request"""
    number: int
    pr_number: int
    repository_full_name: str
    title: str
    created_at: datetime
    closed_at: datetime

    def construct_github_url(self) -> str:
        return GITHUB_DOMAIN + f"{self.repository_full_name}/issues/{self.number}"


@dataclass
class PullRequest:
    """Represents a merged pull request with relevant metadata"""
    number: int
    title: str
    repository: Repository
    merged_at: datetime
    created_at: datetime
    author_login: str
    additions: int = 0
    deletions: int = 0
    merged_by_login: Optional[str] = None
    commits: int = 0
    issues: Optional[List[Issue]] = None
    
    @property
    def repository_full_name(self) -> str:
        """For backward compatibility with existing code"""
        return self.repository.full_name
    
    @property
    def total_changes(self) -> int:
        """Total lines changed (additions + deletions)"""
        return self.additions + self.deletions
    
    def construct_github_url(self) -> str:
        return GITHUB_DOMAIN + f"{self.repository_full_name}/pull/{self.number}"
    
    @classmethod
    def from_graphql_response(cls, pr_data: dict) -> 'PullRequest':
        """Create PullRequest from GraphQL API response"""
        repo_data = pr_data['repository']
        repository = Repository(
            name=repo_data['name'],
            owner=repo_data['owner']['login']
        )

        raw_issues = pr_data['closingIssuesReferences']['nodes']
        issues = []
        for issue in raw_issues:
            if issue['closedAt']:
                issues.append(Issue(
                    number=issue['number'],
                    pr_number=pr_data['number'],
                    repository_full_name=repository.full_name,
                    title=issue['title'],
                    created_at=parse_github_timestamp(issue['createdAt']),
                    closed_at=parse_github_timestamp(issue['closedAt']),
                ))

        return cls(
            number=pr_data['number'],
            title=pr_data['title'],
            repository=repository,
            merged_at=parse_github_timestamp(pr_data['mergedAt']),
            created_at=parse_github_timestamp(pr_data['createdAt']),
            additions=pr_data['additions'],
            deletions=pr_data['deletions'],
            author_login=pr_data['author']['login'],
            merged_by_login=pr_data['mergedBy']['login'] if pr_data.get('mergedBy') else None,
            commits=pr_data.get('commits', {}).get('totalCount', 0),
            issues=issues
        )


@dataclass
class MinerEvaluation:
    uid: int
    github_id: Optional[str] = None
    github_pat: Optional[str] = None
    failed_reason: Optional[str] = None
    valid_prs: List['PRDiff'] = field(default_factory=list)
    unique_repos_contributed_to: Set[str] = field(default_factory=set)
    total_score: float = 0.0
    total_lines_changed: int = 0
    total_open_prs: int = 0
    
    @property
    def total_prs(self) -> int:
        """Total number of valid PRs"""
        return len(self.valid_prs)
    
    def calculate_metric_totals(self):
        """Calculate total lines changed and unique repositories from PRs"""
        if not self.valid_prs:
            return
        
        self.total_lines_changed = sum(pr.total_changes for pr in self.valid_prs)
        self.unique_repos_contributed_to = set(pr.repository_full_name for pr in self.valid_prs)
    
    def calculate_score_total(self):
        """Calculate total score by summing earned scores from all PRs"""
        self.total_score = sum(pr.earned_score for pr in self.valid_prs)

    def apply_open_pr_spam_penalty(self, threshold: int, min_weight: float, penalty_slope: float):
        """
        Apply penalty for excessive open PRs with configurable parameters.
        
        Args:
            threshold: Number of open PRs before penalty kicks in
            min_weight: Minimum weight (maximum penalty)
            penalty_slope: How steep the penalty curve is
        """
        if self.total_open_prs <= threshold:
            return 1.0
        weight = max(min_weight, 1.0 - self.total_open_prs * penalty_slope)
        self.total_score = weight * self.total_score

    def set_evaluation_failed_reason(self, reason: str, logger_func: Optional[Callable] = None):
        """
        Sets the reason for why a miners evaluation may have failed.
        
        Args:
            reason: The failure reason
            logger_func: Optional logging function to use (defaults to print)
        """
        if logger_func:
            logger_func(reason)
            logger_func("*" * 50)
        else:
            print(reason)
            print("*" * 50)
        self.failed_reason = reason
