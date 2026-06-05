-- MkopoSwift PIMS - ISO/IEC 27701:2025 Standalone Schema (PostgreSQL)
-- A.7.2.2 Data Minimisation & A.7.2.1 Consent Management
-- Kenyan DPA 2019 Section 30 and 43

-- Enable UUID extension for synthetic IDs (optional but recommended)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active','suspended','deleted'))
);

CREATE TABLE user_metadata (
    meta_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    purpose_id VARCHAR(50) NOT NULL,
    national_id VARCHAR(20) NOT NULL
        CHECK (length(national_id) BETWEEN 7 AND 20),
    phone_number VARCHAR(13) NOT NULL
        CHECK (length(phone_number) BETWEEN 10 AND 13),
    biometric_hash VARCHAR(64),
    UNIQUE(user_id, purpose_id)
);

CREATE TABLE consent_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    purpose_id VARCHAR(50) NOT NULL,
    consent_given SMALLINT NOT NULL CHECK (consent_given IN (0,1)),
    consent_terms_hash VARCHAR(64) NOT NULL,
    consent_signature TEXT NOT NULL,
    ip_address INET NOT NULL,
    consent_timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Immutability triggers (PL/pgSQL)
CREATE OR REPLACE FUNCTION block_consent_mutation() RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Consent logs are immutable – DELETE/UPDATE forbidden per KDPA §30.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_consent_update
    BEFORE UPDATE ON consent_logs
    FOR EACH ROW EXECUTE FUNCTION block_consent_mutation();

CREATE TRIGGER prevent_consent_delete
    BEFORE DELETE ON consent_logs
    FOR EACH ROW EXECUTE FUNCTION block_consent_mutation();

CREATE INDEX idx_consent_time ON consent_logs(consent_timestamp);