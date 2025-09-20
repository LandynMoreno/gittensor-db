-- File changes table
-- Stores individual file changes from classes.py FileChange dataclass

CREATE TABLE IF NOT EXISTS file_changes (
    id               BIGSERIAL        PRIMARY KEY,
    pr_diff_id       BIGINT           NOT NULL,
    filename         VARCHAR(500)     NOT NULL,
    changes          INTEGER          DEFAULT 0,
    additions        INTEGER          DEFAULT 0,
    deletions        INTEGER          DEFAULT 0,
    status           VARCHAR(50)      NOT NULL,
    file_extension   VARCHAR(50)      NOT NULL DEFAULT '',
    patch            TEXT,

    -- Metadata with automatic timestamps
    created_at       TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint
    FOREIGN KEY (pr_diff_id)
        REFERENCES pr_diffs(id)
            ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_file_changes_pr_diff_id    IF NOT EXISTS ON    file_changes (pr_diff_id);