"""
Repository for handling database operations for PullRequest entities
"""
from typing import Optional, List, Dict, Any
from ..models.domain_models import PullRequest, Repository, PRDiff, FileChange
from .base_repository import BaseRepository
from ..queries import (
    GET_PULL_REQUEST,
    SET_PULL_REQUEST,
    GET_PULL_REQUESTS_BY_REPOSITORY,
    GET_PULL_REQUEST_WITH_DIFFS
)


class PullRequestsRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def _map_to_pull_request(self, row: Dict[str, Any]) -> PullRequest:
        """Map database row to PullRequest object"""
        repository = Repository(
            name=row['name'],
            owner=row['owner']
        )

        return PullRequest(
            number=row['number'],
            title=row['title'],
            repository=repository,
            merged_at=row['merged_at'],
            created_at=row['pr_created_at'],
            additions=row['additions'],
            deletions=row['deletions'],
            commits=row.get('commits', 0),
            author_login=row['author_login'],
            merged_by_login=row['merged_by_login']
        )

    def _map_to_pull_request_with_diffs(self, rows: List[Dict[str, Any]]) -> Optional[PullRequest]:
        """Map database rows to PullRequest with nested PRDiff and FileChanges"""
        if not rows:
            return None

        first_row = rows[0]
        repository = Repository(
            name=first_row['name'],
            owner=first_row['owner']
        )

        pull_request = PullRequest(
            number=first_row['number'],
            title=first_row['title'],
            repository=repository,
            merged_at=first_row['merged_at'],
            created_at=first_row['pr_created_at'],
            additions=first_row['additions'],
            deletions=first_row['deletions'],
            commits=first_row.get('commits', 0),
            author_login=first_row['author_login'],
            merged_by_login=first_row['merged_by_login']
        )

        # Create nested PRDiff with FileChanges if they exist
        if first_row.get('filename'):  # Check if file changes exist
            file_changes = []
            for row in rows:
                if row['filename']:  # Skip rows without file changes
                    file_change = FileChange(
                        filename=row['filename'],
                        changes=row['changes'],
                        additions=row['file_additions'],
                        deletions=row['file_deletions'],
                        status=row['status'],
                        patch=row['patch'],
                        file_extension=row['file_extension']
                    )
                    file_changes.append(file_change)

            # Attach PRDiff to pull_request (we'll need to add this as an attribute)
            pull_request.pr_diff = PRDiff(
                pr_number=pull_request.number,
                repository_full_name=pull_request.repository_full_name,
                files=file_changes,
                earned_score=first_row.get('earned_score', 0.0)
            )

        return pull_request

    def get_pull_request(self, pr_number: int, repository_full_name: str) -> Optional[PullRequest]:
        """
        Get a pull request by its number and repository

        Args:
            pr_number: PR number
            repository_full_name: Full repository name

        Returns:
            PullRequest object if found, None otherwise
        """
        return self.query_single(GET_PULL_REQUEST, (pr_number, repository_full_name), self._map_to_pull_request)

    def set_pull_request(self, pull_request: PullRequest) -> bool:
        """
        Insert or update a pull request

        Args:
            pull_request: PullRequest object to store

        Returns:
            True if successful, False otherwise
        """
        query = SET_PULL_REQUEST
        params = (
            pull_request.number,
            pull_request.repository_full_name,
            pull_request.title,
            pull_request.merged_at,
            pull_request.created_at,
            pull_request.additions,
            pull_request.deletions,
            pull_request.commits,
            pull_request.author_login,
            pull_request.merged_by_login
        )
        return self.set_entity(query, params)

    def get_pull_requests_by_repository(self, repository_full_name: str) -> List[PullRequest]:
        """
        Get all pull requests for a specific repository

        Args:
            repository_full_name: Full repository name

        Returns:
            List of PullRequest objects
        """
        return self.query_multiple(GET_PULL_REQUESTS_BY_REPOSITORY, (repository_full_name,), self._map_to_pull_request)

    def get_pull_request_with_diffs(self, pr_number: int, repository_full_name: str) -> Optional[PullRequest]:
        """
        Get a pull request with its associated PR diffs and file changes.

        This method efficiently loads nested objects in a single query using JOINs,
        which is a common practice for eager loading of related data.

        Args:
            pr_number: PR number
            repository_full_name: Full repository name

        Returns:
            PullRequest object with nested PRDiff and FileChanges, or None if not found
        """
        results = self.execute_query(GET_PULL_REQUEST_WITH_DIFFS, (pr_number, repository_full_name))
        return self._map_to_pull_request_with_diffs(results)

    def get_pull_requests_by_repository_with_diffs(self, repository_full_name: str) -> List[PullRequest]:
        """
        Get all pull requests for a repository with their associated diffs and file changes.

        Note: This can be memory intensive for repositories with many PRs and large diffs.
        Consider pagination for production use.

        Args:
            repository_full_name: Full repository name

        Returns:
            List of PullRequest objects with nested data
        """
        # Modify query to get all PRs for repository
        query = GET_PULL_REQUEST_WITH_DIFFS.replace(
            "WHERE pr.number = %s AND pr.repository_full_name = %s",
            "WHERE pr.repository_full_name = %s ORDER BY pr.merged_at DESC"
        )

        results = self.execute_query(query, (repository_full_name,))

        # Group results by PR number to handle multiple file changes per PR
        pr_groups = {}
        for result in results:
            pr_key = result['number']
            if pr_key not in pr_groups:
                pr_groups[pr_key] = []
            pr_groups[pr_key].append(result)

        # Map each group to a PullRequest with nested data
        pull_requests = []
        for pr_results in pr_groups.values():
            pr = self._map_to_pull_request_with_diffs(pr_results)
            if pr:
                pull_requests.append(pr)

        return pull_requests