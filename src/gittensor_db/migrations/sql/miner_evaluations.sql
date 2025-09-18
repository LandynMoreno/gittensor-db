-- Miner evaluation results table
-- Stores complete validator assessment results from classes.py MinerEvaluation dataclass

CREATE TABLE IF NOT EXISTS miner_evaluations (
    id                   BIGSERIAL        PRIMARY KEY,
    uid                  INTEGER          NOT NULL,
    github_id            VARCHAR(255),
    failed_reason        TEXT,
    total_score          DECIMAL(15,6)    DEFAULT 0.0,
    total_lines_changed  INTEGER          DEFAULT 0,
    total_open_prs       INTEGER          DEFAULT 0,
    total_prs            INTEGER          DEFAULT 0,
    unique_repos_count   INTEGER          DEFAULT 0,

    -- Metadata with automatic timestamps
    evaluation_timestamp TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    created_at           TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,

    -- Unique constraint to prevent duplicate evaluations
    CONSTRAINT unique_evaluation UNIQUE (uid, evaluation_timestamp)
);

-- Indexes for performance
CREATE INDEX idx_miner_evaluations_uid ON miner_evaluations(uid);
CREATE INDEX dx_miner_evaluations_evaluation_timestamp ON miner_evaluations(evaluation_timestamp);