# Repository Queries
GET_REPOSITORY = """
SELECT full_name, name, owner
FROM repositories
WHERE full_name = %s
"""

SET_REPOSITORY = """
INSERT INTO repositories (full_name, name, owner)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    owner = VALUES(owner)
"""

GET_ALL_REPOSITORIES = """
SELECT full_name, name, owner
FROM repositories
ORDER BY full_name
"""

# Pull Request Queries
GET_PULL_REQUEST = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.created_at_pr, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.number = %s AND pr.repository_full_name = %s
"""

SET_PULL_REQUEST = """
INSERT INTO pull_requests (
    number, repository_full_name, title, merged_at, created_at_pr,
    additions, deletions, commits, author_login, merged_by_login
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    title = VALUES(title),
    merged_at = VALUES(merged_at),
    created_at_pr = VALUES(created_at_pr),
    additions = VALUES(additions),
    deletions = VALUES(deletions),
    commits = VALUES(commits),
    author_login = VALUES(author_login),
    merged_by_login = VALUES(merged_by_login)
"""

GET_PULL_REQUESTS_BY_REPOSITORY = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.created_at_pr, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.repository_full_name = %s
ORDER BY pr.merged_at DESC
"""

GET_PULL_REQUEST_WITH_DIFFS = """
SELECT pr.number, pr.title, pr.repository_full_name, pr.merged_at,
       pr.created_at_pr, pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner,
       pd.evaluation_id, pd.earned_score,
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
SELECT id, pr_number, repository_full_name, evaluation_id, earned_score, created_at
FROM pr_diffs
WHERE pr_number = %s AND repository_full_name = %s AND evaluation_id = %s
"""

SET_PR_DIFF = """
INSERT INTO pr_diffs (
    pr_number, repository_full_name, evaluation_id, earned_score
) VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    earned_score = VALUES(earned_score),
    updated_at = CURRENT_TIMESTAMP
"""

GET_PR_DIFFS_BY_EVALUATION = """
SELECT pd.id, pd.pr_number, pd.repository_full_name, pd.evaluation_id, pd.earned_score, pd.created_at,
       pr.title, pr.merged_at, pr.created_at_pr, pr.additions, pr.deletions,
       pr.author_login, pr.merged_by_login
FROM pr_diffs pd
JOIN pull_requests pr ON pd.pr_number = pr.number AND pd.repository_full_name = pr.repository_full_name
WHERE pd.evaluation_id = %s
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
ON DUPLICATE KEY UPDATE
    changes = VALUES(changes),
    additions = VALUES(additions),
    deletions = VALUES(deletions),
    status = VALUES(status),
    patch = VALUES(patch),
    file_extension = VALUES(file_extension),
    updated_at = CURRENT_TIMESTAMP
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
ORDER BY evaluation_timestamp DESC
LIMIT 1
"""

SET_MINER_EVALUATION = """
INSERT INTO miner_evaluations (
    uid, github_id, github_pat_hash, failed_reason, total_score,
    total_lines_changed, total_open_prs, total_prs, unique_repos_count,
    evaluation_timestamp
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
"""

GET_EVALUATIONS_BY_TIMEFRAME = """
SELECT id, uid, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE evaluation_timestamp BETWEEN %s AND %s
ORDER BY evaluation_timestamp DESC, total_score DESC
"""