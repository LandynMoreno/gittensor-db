-- Issues table
-- Stores issue information referenced by pull requests

CREATE TABLE IF NOT EXISTS issues (
    number               INTEGER        PRIMARY KEY,
    pr_number            INTEGER          NOT NULL,
    repository_full_name VARCHAR(255)     NOT NULL,
    title                TEXT             NOT NULL,
    created_at           TIMESTAMP        NOT NULL,
    closed_at            TIMESTAMP        NOT NULL,

    -- Foreign key constraint to pull_requests table
    FOREIGN KEY (pr_number, repository_full_name) REFERENCES pull_requests(number, repository_full_name) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_issues_pr_number ON issues(pr_number);
CREATE INDEX idx_issues_repository ON issues(repository_full_name);