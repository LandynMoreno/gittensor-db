"""
Basic repository tests
"""
import pytest
from src.gittensor_db.repositories import RepositoriesRepository
from src.gittensor_db.models.domain_models import Repository

def test_repositories_repository_init(mock_db_connection):
    """Test repository initialization"""
    repo = RepositoriesRepository(mock_db_connection)
    assert repo.db == mock_db_connection

def test_repository_model():
    """Test Repository domain model"""
    repo = Repository(name="test-repo", owner="test-owner")
    assert repo.full_name == "test-owner/test-repo"
    assert repo.name == "test-repo"
    assert repo.owner == "test-owner"