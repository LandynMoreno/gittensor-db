# Miner Queries
GET_MINER = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
WHERE uid = %s AND hotkey = %s AND github_id = %s
"""

GET_MINER_BY_UID = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
WHERE uid = %s
"""

GET_MINER_BY_HOTKEY = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
WHERE hotkey = %s
"""

GET_MINER_BY_GITHUB_ID = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
WHERE github_id = %s
"""

GET_MINER_BY_HOTKEY_AND_GITHUB_ID = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
WHERE hotkey = %s AND github_id = %s
"""

SET_MINER = """
INSERT INTO miners (uid, hotkey, github_id)
VALUES (%s, %s, %s)
ON CONFLICT (uid, hotkey, github_id)
DO NOTHING
"""

UPSERT_MINER = """
INSERT INTO miners (uid, hotkey, github_id)
VALUES (%s, %s, %s)
ON CONFLICT (uid, hotkey, github_id)
DO UPDATE SET
    updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago'
"""

GET_ALL_MINERS = """
SELECT uid, hotkey, github_id, created_at, updated_at
FROM miners
ORDER BY uid
"""

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
SELECT pr.number, pr.repository_full_name, pr.uid, pr.hotkey, pr.github_id,
       pr.earned_score, pr.title, pr.merged_at, pr.pr_created_at,
       pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.number = %s AND pr.repository_full_name = %s
"""

SET_PULL_REQUEST = """
INSERT INTO pull_requests (
    number, repository_full_name, uid, hotkey, github_id, earned_score,
    title, merged_at, pr_created_at, additions, deletions, commits,
    author_login, merged_by_login
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (number, repository_full_name)
DO NOTHING
"""

GET_PULL_REQUESTS_BY_REPOSITORY = """
SELECT pr.number, pr.repository_full_name, pr.uid, pr.hotkey, pr.github_id,
       pr.earned_score, pr.title, pr.merged_at, pr.pr_created_at,
       pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.repository_full_name = %s
ORDER BY pr.merged_at DESC
"""

GET_PULL_REQUESTS_BY_MINER = """
SELECT pr.number, pr.repository_full_name, pr.uid, pr.hotkey, pr.github_id,
       pr.earned_score, pr.title, pr.merged_at, pr.pr_created_at,
       pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
WHERE pr.uid = %s AND pr.hotkey = %s AND pr.github_id = %s
ORDER BY pr.earned_score DESC, pr.merged_at DESC
"""

GET_PULL_REQUEST_WITH_FILE_CHANGES = """
SELECT pr.number, pr.repository_full_name, pr.uid, pr.hotkey, pr.github_id,
       pr.earned_score, pr.title, pr.merged_at, pr.pr_created_at,
       pr.additions, pr.deletions, pr.commits, pr.author_login,
       pr.merged_by_login, r.name, r.owner,
       fc.filename, fc.changes, fc.additions as file_additions,
       fc.deletions as file_deletions, fc.status, fc.patch, fc.file_extension
FROM pull_requests pr
JOIN repositories r ON pr.repository_full_name = r.full_name
LEFT JOIN file_changes fc ON pr.number = fc.pr_number AND pr.repository_full_name = fc.repository_full_name
WHERE pr.number = %s AND pr.repository_full_name = %s
"""


# File Change Queries
GET_FILE_CHANGE = """
SELECT id, pr_number, repository_full_name, filename, changes, additions, deletions, status, patch, file_extension, created_at
FROM file_changes
WHERE id = %s
"""

GET_FILE_CHANGES_BY_PR = """
SELECT id, pr_number, repository_full_name, filename, changes, additions, deletions, status, patch, file_extension, created_at
FROM file_changes
WHERE pr_number = %s AND repository_full_name = %s
ORDER BY filename
"""

SET_FILE_CHANGES_FOR_PR = """
INSERT INTO file_changes (
    pr_number, repository_full_name, filename, changes, additions, deletions, status, patch, file_extension
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (pr_number, repository_full_name, filename)
DO NOTHING
"""

# Miner Evaluation Queries
GET_MINER_EVALUATION = """
SELECT id, uid, hotkey, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE id = %s
"""

GET_LATEST_MINER_EVALUATION = """
SELECT id, uid, hotkey, github_id, failed_reason, total_score,
       total_lines_changed, total_open_prs, total_prs,
       unique_repos_count, evaluation_timestamp
FROM miner_evaluations
WHERE uid = %s AND hotkey = %s
ORDER BY evaluation_timestamp DESC NULLS LAST, id DESC
LIMIT 1
"""

SET_MINER_EVALUATION = """
INSERT INTO miner_evaluations (
    uid, hotkey, github_id, failed_reason, total_score,
    total_lines_changed, total_open_prs, total_prs, unique_repos_count
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_EVALUATIONS_BY_TIMEFRAME = """
SELECT id, uid, hotkey, github_id, failed_reason, total_score,
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
BULK_UPSERT_MINERS = """
INSERT INTO miners (uid, hotkey, github_id)
VALUES %s
ON CONFLICT (uid, hotkey, github_id)
DO UPDATE SET
    updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago'
"""

BULK_UPSERT_REPOSITORIES = """
INSERT INTO repositories (full_name, name, owner)
VALUES %s
ON CONFLICT (full_name)
DO NOTHING
"""

BULK_UPSERT_PULL_REQUESTS = """
INSERT INTO pull_requests (
    number, repository_full_name, uid, hotkey, github_id, earned_score,
    title, merged_at, pr_created_at, additions, deletions, commits,
    author_login, merged_by_login
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


BULK_UPSERT_FILE_CHANGES = """
INSERT INTO file_changes (
    pr_number, repository_full_name, filename, changes, additions, deletions, status, patch, file_extension
) VALUES %s
ON CONFLICT (pr_number, repository_full_name, filename)
DO NOTHING
"""