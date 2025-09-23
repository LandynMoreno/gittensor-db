-- Repository information table
-- Stores basic repository metadata from classes.py Repository dataclass

CREATE TABLE IF NOT EXISTS repositories (
    full_name        VARCHAR(255)     PRIMARY KEY,
    name             VARCHAR(255)     NOT NULL,
    owner            VARCHAR(255)     NOT NULL,

    -- Metadata with automatic timestamps
    created_at       TIMESTAMP        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago'),
    updated_at       TIMESTAMP        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'America/Chicago')
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_repositories_name    ON repositories (name);