"""
Basic usage example for gittensor-db package
"""

from gittensor_db import (
    create_database_connection,
    RepositoriesRepository,
    MinerEvaluationsRepository
)
from gittensor_db.models.domain_models import Repository, MinerEvaluation

def main():
    # Create database connection
    db = create_database_connection()
    if not db:
        print("Failed to connect to database")
        return
    
    # Initialize repositories
    repos_repo = RepositoriesRepository(db)
    evaluations_repo = MinerEvaluationsRepository(db)
    
    # Example: Create a repository
    repo = Repository(name="example-repo", owner="example-owner")
    success = repos_repo.set_repository(repo)
    print(f"Repository saved: {success}")
    
    # Example: Get repository
    retrieved_repo = repos_repo.get_repository("example-owner/example-repo")
    if retrieved_repo:
        print(f"Found repo: {retrieved_repo.full_name}")
    
    # Example: Create miner evaluation
    evaluation = MinerEvaluation(
        uid=123,
        github_id="test-user",
        total_score=85.5,
        total_lines_changed=500
    )
    success = evaluations_repo.set_miner_evaluation(evaluation)
    print(f"Evaluation saved: {success}")
    
    # Clean up
    db.close()

if __name__ == "__main__":
    main()