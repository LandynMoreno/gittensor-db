"""
Repository for handling database operations for Repository entities
"""
from typing import Optional, List, Dict, Any
from ..models.domain_models import Repository
from .base_repository import BaseRepository
from ..queries import (
    GET_REPOSITORY,
    SET_REPOSITORY,
    GET_ALL_REPOSITORIES
)


class RepositoriesRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def _map_to_repository(self, row: Dict[str, Any]) -> Repository:
        """Map database row to Repository object"""
        return Repository(
            name=row['name'],
            owner=row['owner']
        )

    def get_repository(self, repository_full_name: str) -> Optional[Repository]:
        """
        Get a repository by its full name

        Args:
            repository_full_name: Full repository name (owner/name)

        Returns:
            Repository object if found, None otherwise
        """
        return self.query_single(GET_REPOSITORY, (repository_full_name,), self._map_to_repository)

    def set_repository(self, repository: Repository) -> bool:
        """
        Insert or update a repository

        Args:
            repository: Repository object to store

        Returns:
            True if successful, False otherwise
        """
        params = (
            repository.full_name,
            repository.name,
            repository.owner
        )
        return self.set_entity(SET_REPOSITORY, params)

    def get_all_repositories(self) -> List[Repository]:
        """
        Get all repositories

        Returns:
            List of Repository objects
        """
        return self.query_multiple(GET_ALL_REPOSITORIES, (), self._map_to_repository)