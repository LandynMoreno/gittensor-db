"""
Repository for handling database operations for FileChange entities
"""
from typing import Optional, List, Dict, Any
from ..models.domain_models import FileChange
from .base_repository import BaseRepository
from ..queries import (
    GET_FILE_CHANGE,
    GET_FILE_CHANGES_BY_PR_DIFF,
    SET_FILE_CHANGES_FOR_PR_DIFF
)


class FileChangesRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def _map_to_file_change(self, row: Dict[str, Any]) -> FileChange:
        """Map database row to FileChange object"""
        return FileChange(
            filename=row['filename'],
            changes=row['changes'],
            additions=row['additions'],
            deletions=row['deletions'],
            status=row['status'],
            patch=row['patch'],
            file_extension=row.get('file_extension'),
            id=row.get('id')
        )

    def get_file_change(self, file_change_id: int) -> Optional[FileChange]:
        """
        Get a file change by its ID

        Args:
            file_change_id: Primary key of the file change

        Returns:
            FileChange object if found, None otherwise
        """
        return self.query_single(GET_FILE_CHANGE, (file_change_id,), self._map_to_file_change)

    def get_file_changes_by_pr_diff(self, pr_diff_id: int) -> List[FileChange]:
        """
        Get all file changes for a specific PR diff

        Args:
            pr_diff_id: Foreign key to PR diff

        Returns:
            List of FileChange objects
        """
        return self.query_multiple(GET_FILE_CHANGES_BY_PR_DIFF, (pr_diff_id,), self._map_to_file_change)

    def set_file_changes_for_pr_diff(self, pr_diff_id: int, file_changes: List[FileChange]) -> bool:
        """
        Set file changes for a specific PR diff.

        This method efficiently stores multiple file changes for a PR diff in a single transaction.
        It will insert new file changes or update existing ones.

        Args:
            pr_diff_id: Foreign key to PR diff
            file_changes: List of FileChange objects to store

        Returns:
            True if all file changes were stored successfully, False otherwise
        """
        if not file_changes:
            return True

        query = SET_FILE_CHANGES_FOR_PR_DIFF

        try:
            with self.get_cursor(dictionary=False) as cursor:
                for file_change in file_changes:
                    params = (
                        pr_diff_id,
                        file_change.filename,
                        file_change.changes,
                        file_change.additions,
                        file_change.deletions,
                        file_change.status,
                        file_change.patch,
                        file_change.file_extension or file_change._calculate_file_extension()
                    )
                    cursor.execute(query, params)

                self.db.commit()
                return True
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error storing file changes for PR diff {pr_diff_id}: {e}")
            return False

    def set_file_change(self, pr_diff_id: int, file_change: FileChange) -> bool:
        """
        Set a single file change for a PR diff.

        Args:
            pr_diff_id: Foreign key to PR diff
            file_change: FileChange object to store

        Returns:
            True if successful, False otherwise
        """
        return self.set_file_changes_for_pr_diff(pr_diff_id, [file_change])