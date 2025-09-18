# examples/complete_workflow.py
"""
Complete workflow example showing all features of gittensor-db
"""
import os
from datetime import datetime
from gittensor_db import (
    create_database_connection,
    test_database_connection,
    DatabaseMigrator,
    RepositoriesRepository,
    PullRequestsRepository,
    MinerEvaluationsRepository
)
from gittensor_db.models.domain_models import (
    Repository, PullRequest, MinerEvaluation
)


def setup_database():
    """Setup database and run migrations"""
    print("Testing database connection...")
    if not test_database_connection():
        print("❌ Database connection failed!")
        return None
    
    print("✅ Database connection successful!")
    
    # Create connection and run migrations
    db = create_database_connection()
    if not db:
        return None
    
    print("Running database migrations...")
    migrator = DatabaseMigrator(db)
    if migrator.migrate():
        print("✅ Database migrations completed!")
    else:
        print("❌ Database migrations failed!")
        return None
    
    return db


def example_workflow():
    """Complete example workflow"""
    # Setup
    db = setup_database()
    if not db:
        return
    
    try:
        # Initialize repositories
        repos_repo = RepositoriesRepository(db)
        prs_repo = PullRequestsRepository(db) 
        evals_repo = MinerEvaluationsRepository(db)
        
        # 1. Create a repository
        print("\n1. Creating repository...")
        repo = Repository(name="awesome-project", owner="gittensor")
        if repos_repo.set_repository(repo):
            print(f"✅ Created repository: {repo.full_name}")
        
        # 2. Create a pull request
        print("\n2. Creating pull request...")
        pr = PullRequest(
            number=42,
            title="Add awesome new feature",
            repository=repo,
            merged_at=datetime.now(),
            created_at=datetime.now(),
            additions=150,
            deletions=20,
            commits=5,
            author_login="awesome-dev"
        )
        if prs_repo.set_pull_request(pr):
            print(f"✅ Created PR #{pr.number}: {pr.title}")
        
        # 3. Create miner evaluation
        print("\n3. Creating miner evaluation...")
        evaluation = MinerEvaluation(
            uid=123,
            github_id="awesome-dev",
            total_score=95.5,
            total_lines_changed=170,
            total_prs=1,
            unique_repos_contributed_to=[repo.full_name]
        )
        if evals_repo.set_miner_evaluation(evaluation):
            print(f"✅ Created evaluation for UID {evaluation.uid}")
        
        # 4. Query data back
        print("\n4. Querying data...")
        
        # Get repository
        retrieved_repo = repos_repo.get_repository(repo.full_name)
        if retrieved_repo:
            print(f"📦 Found repository: {retrieved_repo.full_name}")
        
        # Get pull request  
        retrieved_pr = prs_repo.get_pull_request(pr.number, repo.full_name)
        if retrieved_pr:
            print(f"🔄 Found PR: #{retrieved_pr.number} - {retrieved_pr.title}")
        
        # Get latest evaluation
        latest_eval = evals_repo.get_latest_miner_evaluation(123)
        if latest_eval:
            print(f"📊 Latest evaluation score: {latest_eval.total_score}")
        
        # Get all repositories
        all_repos = repos_repo.get_all_repositories()
        print(f"📋 Total repositories in database: {len(all_repos)}")
        
        print("\n🎉 Workflow completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during workflow: {e}")
        
    finally:
        db.close()


if __name__ == "__main__":
    print("GitTensor DB Package - Complete Workflow Example")
    print("=" * 50)
    
    # Check environment
    required_env = ['DB_HOST', 'DB_USER', 'DB_NAME']
    missing_env = [var for var in required_env if not os.getenv(var)]
    
    if missing_env:
        print(f"❌ Missing environment variables: {', '.join(missing_env)}")
        print("\nPlease set the following environment variables:")
        print("export DB_HOST=localhost")
        print("export DB_USER=your_username") 
        print("export DB_PASSWORD=your_password")
        print("export DB_NAME=gittensor_test")
        print("export DB_PORT=3306  # optional, defaults to 3306")
    else:
        example_workflow()


# examples/quick_test.py  
"""
Quick test to verify package installation and basic functionality
"""
def quick_test():
    """Quick test of package functionality"""
    try:
        # Test imports
        print("Testing imports...")
        from gittensor_db import create_database_connection, test_database_connection
        from gittensor_db.models.domain_models import Repository, MinerEvaluation
        print("✅ All imports successful!")
        
        # Test model creation
        print("Testing model creation...")
        repo = Repository(name="test", owner="test-owner")
        assert repo.full_name == "test-owner/test"
        
        eval = MinerEvaluation(uid=1, total_score=100.0)
        assert eval.uid == 1
        print("✅ Model creation successful!")
        
        # Test database connection (without actually connecting)
        print("Testing connection function availability...")
        assert callable(create_database_connection)
        assert callable(test_database_connection)
        print("✅ Connection functions available!")
        
        print("\n🎉 Package installation verified!")
        print("Now set up your database environment variables and run the complete workflow.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the package is installed: pip install -e .")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    quick_test()