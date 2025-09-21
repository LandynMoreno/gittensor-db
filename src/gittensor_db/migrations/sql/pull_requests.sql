-- Pull request information table
-- Stores PR metadata from classes.py PullRequest dataclass

CREATE TABLE IF NOT EXISTS pull_requests (
    number               INTEGER          NOT NULL,
    repository_full_name VARCHAR(255)     NOT NULL,
    title                TEXT             NOT NULL,
    merged_at            TIMESTAMP        NOT NULL,
    pr_created_at        TIMESTAMP        NOT NULL,
    additions            INTEGER          DEFAULT 0,
    deletions            INTEGER          DEFAULT 0,
    commits              INTEGER          DEFAULT 0,
    author_login         VARCHAR(255)     NOT NULL,
    merged_by_login      VARCHAR(255),

    -- Metadata with automatic timestamps
    created_at           TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (number, repository_full_name),

    -- Foreign key constraint
    FOREIGN KEY (repository_full_name)
        REFERENCES repositories(full_name)
            ON DELETE CASCADE

    -- Data integrity constraints
    CONSTRAINT chk_pull_requests_additions    CHECK    (additions >= 0);
    CONSTRAINT chk_pull_requests_deletions    CHECK    (deletions >= 0);
    CONSTRAINT chk_pull_requests_commits      CHECK    (commits   >= 0);
);

-- Indexes for performance
CREATE INDEX idx_pull_requests_author        IF NOT EXISTS ON    pull_requests (author_login);
CREATE INDEX idx_pull_requests_merged_at     IF NOT EXISTS ON    pull_requests (merged_at);
CREATE INDEX idx_pull_requests_merged_by     IF NOT EXISTS ON    pull_requests (merged_by_login);