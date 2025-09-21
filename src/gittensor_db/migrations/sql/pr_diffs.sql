-- Pull request diff information table
-- Stores diff metadata from classes.py PRDiff dataclass

CREATE TABLE IF NOT EXISTS pr_diffs (
    id                   BIGSERIAL        PRIMARY KEY,
    pr_number            INTEGER          NOT NULL,
    repository_full_name VARCHAR(255)     NOT NULL,
    miner_evaluation_id  BIGINT           NOT NULL,
    earned_score         DECIMAL(15,6)    DEFAULT 0.0,
    total_changes        INTEGER          DEFAULT 0,

    -- Metadata with automatic timestamps
    created_at           TIMESTAMP        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago'),
    updated_at           TIMESTAMP        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago'),

    -- Foreign key constraints
    FOREIGN KEY (pr_number, repository_full_name)
        REFERENCES pull_requests(number, repository_full_name)
            ON DELETE CASCADE,

    FOREIGN KEY (miner_evaluation_id)
        REFERENCES miner_evaluations(id)
            ON DELETE CASCADE,

    -- Unique constraint to prevent duplicate pr_diffs for same evaluation and PR
    CONSTRAINT unique_pr_diff 
        UNIQUE (miner_evaluation_id, pr_number, repository_full_name),

    -- Data integrity constraints
    CONSTRAINT chk_pr_diffs_earned_score     CHECK    (earned_score  >= 0),
    CONSTRAINT chk_pr_diffs_total_changes    CHECK    (total_changes >= 0)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_pr_diffs_miner_evaluation_id    ON pr_diffs (miner_evaluation_id);
CREATE INDEX IF NOT EXISTS idx_pr_diffs_pr_number              ON pr_diffs (pr_number);
CREATE INDEX IF NOT EXISTS idx_pr_diffs_repository_name        ON pr_diffs (repository_full_name);
CREATE INDEX IF NOT EXISTS idx_pr_diffs_earned_score           ON pr_diffs (earned_score);
CREATE INDEX IF NOT EXISTS idx_pr_diffs_total_changes          ON pr_diffs (total_changes);