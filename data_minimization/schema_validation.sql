-- MkopoSwift PIMS - ISO/IEC 27701:2025 Standalone Schema
-- A.7.2.2 Data Minimisation & A.7.2.1 Consent Management
-- Kenyan DPA 2019 Section 30 (Consent) and Section 43 (Notification)

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','suspended','deleted'))
);

CREATE TABLE user_metadata (
    meta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    purpose_id TEXT NOT NULL,
    national_id TEXT NOT NULL CHECK(length(national_id) BETWEEN 7 AND 20),
    phone_number TEXT NOT NULL CHECK(length(phone_number) BETWEEN 10 AND 13),
    biometric_hash TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, purpose_id)
);

CREATE TABLE consent_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    purpose_id TEXT NOT NULL,
    consent_given INTEGER NOT NULL CHECK(consent_given IN (0,1)),
    consent_terms_hash TEXT NOT NULL,
    consent_signature TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    consent_timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TRIGGER prevent_consent_mutation
BEFORE UPDATE ON consent_logs
BEGIN
    SELECT RAISE(FAIL, 'Consent logs are immutable – DELETE/UPDATE forbidden per KDPA §30.');
END;

CREATE TRIGGER prevent_consent_deletion
BEFORE DELETE ON consent_logs
BEGIN
    SELECT RAISE(FAIL, 'Consent logs are immutable – DELETE/UPDATE forbidden per KDPA §30.');
END;

CREATE INDEX idx_consent_time ON consent_logs(consent_timestamp);