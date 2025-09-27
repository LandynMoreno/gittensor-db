"""
Repository for handling database operations for PRDiff entities
"""
from typing import Optional, List, Dict, Any
from ..models.domain_models import PRDiff
from .base_repository import BaseRepository
from .file_changes_repository import FileChangesRepository
from ..queries import (
    GET_PR_DIFF_METADATA,
    SET_PR_DIFF,
    GET_PR_DIFFS_BY_EVALUATION,
    BULK_UPSERT_PR_DIFFS
)


class PRDiffsRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.file_changes_repo = FileChangesRepository(db_connection)

    def _map_to_pr_diff_metadata(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Map database row to PR diff metadata dictionary"""
        return {
            'id': row['id'],
            'pr_number': row['pr_number'],
            'repository_full_name': row['repository_full_name'],
            'earned_score': float(row['earned_score']) if row['earned_score'] else 0.0
        }

    def get_pr_diff(self, pr_diff_id: int) -> Optional[PRDiff]:
        """
        Get a PR diff by its ID

        Args:
            pr_diff_id: Primary key of the PR diff

        Returns:
            PRDiff object if found, None otherwise
        """
        # Get PR diff metadata
        diff_metadata = self.query_single(GET_PR_DIFF_METADATA, (pr_diff_id,), self._map_to_pr_diff_metadata)

        if not diff_metadata:
            return None

        # Get associated file changes
        files = self.file_changes_repo.get_file_changes_by_pr_diff(pr_diff_id)

        return PRDiff(
            pr_number=diff_metadata['pr_number'],
            repository_full_name=diff_metadata['repository_full_name'],
            files=files,
            earned_score=diff_metadata['earned_score']
        )

    def set_pr_diff(self, pr_diff: PRDiff, miner_evaluation_id: int) -> Optional[int]:
        """
        Insert a new PR diff and its associated file changes

        Args:
            pr_diff: PRDiff object to store
            miner_evaluation_id: Foreign key to miner evaluation

        Returns:
            PR diff ID if successful, None otherwise
        """
        try:
            # Insert PR diff metadata
            query = SET_PR_DIFF
            params = (
                pr_diff.pr_number,
                pr_diff.repository_full_name,
                miner_evaluation_id,
                pr_diff.earned_score
            )

            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                pr_diff_id = cursor.lastrowid
                self.db.commit()

                # Insert file changes using the file changes repository
                if pr_diff.files:
                    success = self.file_changes_repo.set_file_changes_for_pr_diff(pr_diff_id, pr_diff.files)
                    if not success:
                        # Rollback the PR diff if file changes failed
                        self.db.rollback()
                        return None

                return pr_diff_id

        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error storing PR diff: {e}")
            return None

    def get_pr_diffs_by_evaluation(self, miner_evaluation_id: int) -> List[PRDiff]:
        """
        Get all PR diffs for a specific miner evaluation

        Args:
            miner_evaluation_id: Foreign key to miner evaluation

        Returns:
            List of PRDiff objects
        """
        # Get all PR diff metadata for the evaluation
        diff_metadata_list = self.query_multiple(GET_PR_DIFFS_BY_EVALUATION, (miner_evaluation_id,), self._map_to_pr_diff_metadata)

        pr_diffs = []
        for diff_metadata in diff_metadata_list:
            # Get file changes for this PR diff
            files = self.file_changes_repo.get_file_changes_by_pr_diff(diff_metadata['id'])

            pr_diff = PRDiff(
                pr_number=diff_metadata['pr_number'],
                repository_full_name=diff_metadata['repository_full_name'],
                files=files,
                earned_score=diff_metadata['earned_score']
            )
            pr_diffs.append(pr_diff)

        return pr_diffs

    def store_pr_diffs_bulk(self, pr_diffs: List[PRDiff]) -> int:
        """
        Bulk insert/update PR diffs with efficient SQL conflict resolution

        Args:
            pr_diffs: List of PRDiff objects to store

        Returns:
            Count of successfully stored PR diffs
        """
        if not pr_diffs:
            return 0

        # Prepare data for bulk insert
        values = []
        for pr_diff in pr_diffs:
            values.append((
                pr_diff.pr_number,
                pr_diff.repository_full_name,
                None,  # miner_evaluation_id - not needed for bulk storage
                pr_diff.earned_score,
                pr_diff.total_changes
            ))

        try:
            with self.get_cursor() as cursor:
                # Use psycopg2's execute_values for efficient bulk insert
                from psycopg2.extras import execute_values
                execute_values(
                    cursor,
                    BULK_UPSERT_PR_DIFFS.replace('VALUES %s', 'VALUES %s'),
                    values,
                    template=None,
                    page_size=100
                )
                self.db.commit()
                return len(values)
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error in bulk PR diff storage: {e}")
            return 0