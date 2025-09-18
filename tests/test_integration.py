"""
Integration tests for gittensor-db package
File: tests/test_integration.py
"""
import pytest
import os
from datetime import datetime
from src.gittensor_db import (
    create_database_connection,
    RepositoriesRepository,
    MinerEvaluationsRepository,
    PullRequestsRepository
)
from src.gittensor_db.models.domain_models import Repository, MinerEvaluation, PullRequest


class TestIntegration:
    """Integration tests that require a real database connection"""
    
    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Setup test database connection"""
        # Only run if test database is configured
        if not all([
            os.getenv('TEST_DB_HOST'),
            os.getenv('TEST_DB_USER'),
            os.getenv('TEST_DB_NAME')
        ]):
            pytest.skip("Test database not configured")
        
        # Temporarily override env vars for test DB
        self.original_env = {}
        test_vars = {
            'DB_HOST': os.getenv('TEST_DB_HOST'),
            'DB_USER': os.getenv('TEST_DB_USER'),
            'DB_PASSWORD': os.getenv('TEST_DB_PASSWORD', ''),
            'DB_NAME': os.getenv('TEST_DB_NAME'),
            'DB_PORT': os.getenv('TEST_DB_PORT', '5432')  # PostgreSQL default
        }
        
        for key, value in test_vars.items():
            self.original_env[key] = os.getenv(key)
            os.environ[key] = value
        
        self.db = create_database_connection()
        if not self.db:
            pytest.skip("Could not connect to test database")
            
        yield
        
        # Cleanup
        if self.db:
            self.db.close()
        
        # Restore original env vars
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_repository_crud(self):
        """Test repository CRUD operations"""
        repo_repo = RepositoriesRepository(self.db)
        
        # Create
        repo = Repository(name="test-repo", owner="test-owner")
        assert repo_repo.set_repository(repo) == True
        
        # Read
        retrieved = repo_repo.get_repository("test-owner/test-repo")
        assert retrieved is not None
        assert retrieved.name == "test-repo"
        assert retrieved.owner == "test-owner"