"""
GitTensor Database Layer

A shared database abstraction layer for GitTensor validator and API services.
"""

from .connection.database import create_database_connection, test_database_connection
from .migrations.migrator import DatabaseMigrator
from .repositories import (
    BaseRepository,
    MinersRepository,
    RepositoriesRepository,
    PullRequestsRepository,
    IssuesRepository,
    FileChangesRepository,
    MinerEvaluationsRepository,
)

__version__ = "0.1.0"
__all__ = [
    "create_database_connection",
    "test_database_connection",
    "BaseRepository",
    "DatabaseMigrator",
    "MinersRepository",
    "RepositoriesRepository",
    "PullRequestsRepository",
    "IssuesRepository",
    "FileChangesRepository",
    "MinerEvaluationsRepository",
]