# Repository Queries
GET_REPOSITORY = """
SELECT full_name, name, owner
FROM repositories
WHERE full_name = %s
"""

SET_REPOSITORY = """
INSERT INTO repositories (full_name, name, owner)
VALUES (%s, %s, %s)
ON CONFLICT (full_name) 
DO NOTHING
"""

GET_ALL_REPOSITORIES = """
SELECT full_name, name, owner
FROM repositories
ORDER BY full_name
"""

# Pull Request Queries
GET_PULL_REQUEST = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.pr_created_at, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.number = %s AND pr.repository_full_name = %s
"""

SET_PULL_REQUEST = """
INSERT INTO pull_requests (
    number, repository_full_name, title, merged_at, pr_created_at,
    additions, deletions, commits, author_login, merged_by_login
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (number, repository_full_name)
DO NOTHING
"""

GET_PULL_REQUESTS_BY_REPOSITORY = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.pr_created_at, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.repository_full_name = %s
ORDER BY pr.merged_at DESC
"""

GET_PULL_REQUEST_WITH_DIFFS = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.pr_created_at, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner,
       pd.miner_evaluation_id, pd.earned_score, pd.total_changes,
       fc.filename, fc.changes, fc.additions as file_additions,
       fc.deletions as file_deletions, fc.status, fc.patch, fc.file_extension
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
LEFT JOIN pr_diffs pd ON pr.number = pd.pr_number AND pr.repository_full_name = pd.repository_full_name
LEFT JOIN file_changes fc ON pd.id = fc.pr_diff_id
WHERE pr.number = %s AND pr.repository_full_name = %s
"""

# PR Diff Queries
GET_PR_DIFF_METADATA = """
SELECT id, pr_number, repository_full_name, miner_evaluation_id, earned_score, total_changes, created_at
FROM pr_diffs
WHERE pr_number = %s AND repository_full_name = %s AND miner_evaluation_id = %s
"""

SET_PR_DIFF = """
INSERT INTO pr_diffs (
    pr_number, repository_full_name, miner_evaluation_id, earned_score, total_changes
) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (miner_evaluation_id, pr_number, repository_full_name) 
DO NOTHING
"""

GET_PR_DIFFS_BY_EVALUATION = """
SELECT pd.id, pd.pr_number, pd.repository_full_name, pd.miner_evaluation_id, pd.earned_score, pd.total_changes, pd.created_at,
       pr.title, pr.merged_at, pr.pr_created_at, pr.additions, pr.deletions,
       pr.author_login, pr.merged_by_login
FROM pr_diffs pd
JOIN pull_requests pr ON pd.pr_number = pr.number AND pd.repository_full_name = pr.repository_full_name
WHERE pd.miner_evaluation_id = %s
ORDER BY pd.earned_score DESC, pr.merged_at DESC
"""

# File Change Queries
GET_FILE_CHANGE = """
SELECT id, pr_diff_id, filename, changes, additions, deletions, status, patch, file_extension, created_at
FROM file_changes
WHERE id = %s
"""

GET_FILE_CHANGES_BY_PR_DIFF = """
SELECT id, pr_diff_id, filename, changes, additions, deletions, status, patch, file_extension, created_at
FROM file_changes
WHERE pr_diff_id = %s
ORDER BY filename
"""

SET_FILE_CHANGES_FOR_PR_DIFF = """
INSERT INTO file_changes (
    pr_diff_id, filename, changes, additions, deletions, status, patch, file_extension
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (pr_diff_id, file_extension)
DO NOTHING
"""

# Miner Evaluation Queries
GET_MINER_EVALUATION = """
SELECT id, uid, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE id = %s
"""

GET_LATEST_MINER_EVALUATION = """
SELECT id, uid, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE uid = %s
ORDER BY evaluation_timestamp DESC NULLS LAST, id DESC
LIMIT 1
"""

SET_MINER_EVALUATION = """
INSERT INTO miner_evaluations (
    uid, github_id, failed_reason, total_score,
    total_lines_changed, total_open_prs, total_prs, unique_repos_count
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_EVALUATIONS_BY_TIMEFRAME = """
SELECT id, uid, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE evaluation_timestamp BETWEEN %s AND %s
ORDER BY evaluation_timestamp DESC, total_score DESC
"""

# Issue Queries
GET_ISSUE = """
SELECT number, pr_number, repository_full_name, title, created_at, closed_at
FROM issues
WHERE number = %s AND repository_full_name = %s
"""

GET_ISSUES_BY_REPOSITORY = """
SELECT number, pr_number, repository_full_name, title, created_at, closed_at
FROM issues
WHERE repository_full_name = %s
ORDER BY created_at DESC
"""

SET_ISSUE = """
INSERT INTO issues (
    number, pr_number, repository_full_name, title, created_at, closed_at
) VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (number, repository_full_name)
DO NOTHING
"""

# Bulk Upsert Queries
BULK_UPSERT_REPOSITORIES = """
INSERT INTO repositories (full_name, name, owner)
VALUES %s
ON CONFLICT (full_name)
DO NOTHING
"""

BULK_UPSERT_PULL_REQUESTS = """
INSERT INTO pull_requests (
    number, repository_full_name, title, merged_at, pr_created_at,
    additions, deletions, commits, author_login, merged_by_login
) VALUES %s
ON CONFLICT (number, repository_full_name)
DO NOTHING
"""

BULK_UPSERT_ISSUES = """
INSERT INTO issues (
    number, pr_number, repository_full_name, title, created_at, closed_at
) VALUES %s
ON CONFLICT (number, repository_full_name)
DO NOTHING
"""

BULK_UPSERT_PR_DIFFS = """
INSERT INTO pr_diffs (
    pr_number, repository_full_name, miner_evaluation_id, earned_score, total_changes
) VALUES %s
ON CONFLICT (miner_evaluation_id, pr_number, repository_full_name)
DO NOTHING
"""

BULK_UPSERT_FILE_CHANGES = """
INSERT INTO file_changes (
    pr_diff_id, filename, changes, additions, deletions, status, patch, file_extension
) VALUES %s
ON CONFLICT (pr_diff_id, filename)
DO NOTHING
"""