CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,               -- Unique identifier for each job
    source VARCHAR(50) NOT NULL,         -- Source of the job (e.g., "hellowork", "wttj", "indeed", "france_travail")
    title VARCHAR(255) NOT NULL,         -- Job title
    company VARCHAR(255),                -- Company name
    location VARCHAR(255),               -- Job location
    contract VARCHAR(100),               -- Contract type (e.g., "CDI", "CDD")
    duration VARCHAR(100),               -- Duration of the job (if applicable)
    date VARCHAR(100),                   -- Date of publication
    offer_url TEXT NOT NULL,             -- URL to the job offer
    created_at TIMESTAMP DEFAULT NOW(),  -- Timestamp for when the job was added to the database
    updated_at TIMESTAMP DEFAULT NOW(),  -- Timestamp for the last update of the job
    status VARCHAR(20) DEFAULT 'active'  -- Status of the job (e.g., "active", "archived")
);

-- Index on the source column for faster queries
CREATE INDEX idx_jobs_source ON jobs (source);

-- Index on the title column for faster queries
CREATE INDEX idx_jobs_title ON jobs (title);