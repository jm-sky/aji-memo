-- AjiMemo Database Schema
-- PostgreSQL

-- Users and authentication
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    plan VARCHAR(20) DEFAULT 'free', -- free, premium, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- API tokens (JWT support)
CREATE TABLE api_tokens (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    token_name VARCHAR(100) NOT NULL,
    token_hash VARCHAR(255) NOT NULL, -- Hash of the actual token
    permissions JSONB DEFAULT '{}', -- Permissions object
    rate_limit_per_hour INTEGER DEFAULT 5, -- Based on user plan
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- API usage tracking
CREATE TABLE api_usage (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    token_id BIGINT REFERENCES api_tokens(id) ON DELETE CASCADE,
    endpoint VARCHAR(100) NOT NULL,
    response_status INTEGER NOT NULL,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Indexes for performance
CREATE INDEX idx_api_usage_user_id_created_at ON api_usage(user_id, created_at);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at);
