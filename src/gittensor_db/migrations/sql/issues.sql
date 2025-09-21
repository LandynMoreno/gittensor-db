-- Issues table
-- Stores issue information referenced by pull requests

CREATE TABLE IF NOT EXISTS issues (
    number               INTEGER          NOT NULL,
    pr_number            INTEGER          NOT NULL,
    repository_full_name VARCHAR(255)     NOT NULL,
    title                TEXT             NOT NULL,
    created_at           TIMESTAMP        NOT NULL,
    closed_at            TIMESTAMP        NOT NULL,

    PRIMARY KEY (number, repository_full_name),

    -- Foreign key constraint
    FOREIGN KEY (pr_number, repository_full_name)
        REFERENCES pull_requests(number, repository_full_name)
            ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_issues_pr_number     IF NOT EXISTS ON    issues (pr_number);
CREATE INDEX idx_issues_repository    IF NOT EXISTS ON    issues (repository_full_name);
CREATE INDEX idx_issues_created_at    IF NOT EXISTS ON    issues (created_at);
CREATE INDEX idx_issues_closed_at     IF NOT EXISTS ON    issues (closed_at);