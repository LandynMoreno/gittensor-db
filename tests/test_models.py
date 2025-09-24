"""
Test domain models
File: tests/test_models.py
"""
from src.gittensor_db.models.domain_models import (
    Repository, FileChange, MinerEvaluation
)


def test_repository_model():
    """Test Repository model"""
    repo = Repository(name="my-repo", owner="my-owner")
    assert repo.full_name == "my-owner/my-repo"


def test_file_change_model():
    """Test FileChange model"""
    file_change = FileChange(
        filename="src/main.py",
        changes=10,
        additions=8,
        deletions=2,
        status="modified"
    )
    assert file_change.filename == "src/main.py"
    assert file_change._calculate_file_extension() == "py"


def test_miner_evaluation_model():
    """Test MinerEvaluation model"""
    evaluation = MinerEvaluation(
        uid=42,
        id=1,  # Required field
        github_id="test-miner",
        total_score=95.0,
        unique_repos_contributed_to={"repo1", "repo2", "repo3"},
        unique_repos_count=3
    )
    assert evaluation.uid == 42
    assert evaluation.id == 1
    assert len(evaluation.unique_repos_contributed_to) == 3
    assert evaluation.unique_repos_count == 3