"""
Repository for handling database operations for Issue entities
"""
from typing import Optional, List, Dict, Any
from ..models.domain_models import Issue
from .base_repository import BaseRepository
from ..queries import (
    GET_ISSUE,
    GET_ISSUES_BY_REPOSITORY,
    SET_ISSUE
)


class IssuesRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def _map_to_issue(self, row: Dict[str, Any]) -> Issue:
        """Map database row to Issue object"""
        return Issue(
            number=row['number'],
            pr_number=row['pr_number'],
            repository_full_name=row['repository_full_name'],
            title=row['title'],
            created_at=row['created_at'],
            closed_at=row['closed_at']
        )

    def get_issue(self, number: int, repository_full_name: str) -> Optional[Issue]:
        """
        Get an issue by its number and repository

        Args:
            number: Issue number
            repository_full_name: Full repository name (owner/name)

        Returns:
            Issue object if found, None otherwise
        """
        return self.query_single(GET_ISSUE, (number, repository_full_name), self._map_to_issue)

    def get_issues_by_repository(self, repository_full_name: str) -> List[Issue]:
        """
        Get all issues for a given repository

        Args:
            repository_full_name: Full repository name (owner/name)

        Returns:
            List of Issue objects
        """
        return self.query_multiple(GET_ISSUES_BY_REPOSITORY, (repository_full_name,), self._map_to_issue)

    def set_issue(self, issue: Issue) -> bool:
        """
        Insert or update an issue

        Args:
            issue: Issue object to store

        Returns:
            True if successful, False otherwise
        """
        params = (
            issue.number,
            issue.pr_number,
            issue.repository_full_name,
            issue.title,
            issue.created_at,
            issue.closed_at
        )
        return self.set_entity(SET_ISSUE, params)