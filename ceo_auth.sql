
-- ============================================================
-- CEO AUTHENTICATION SCHEMA
-- ============================================================
CREATE TABLE IF NOT EXISTS ceo_accounts (
    id              BIGSERIAL PRIMARY KEY,
    username        VARCHAR(64) NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ceo_accounts_username
    ON ceo_accounts (username);

CREATE INDEX IF NOT EXISTS idx_ceo_accounts_active
    ON ceo_accounts (is_active);

-- Update timestamp otomatis ketika row berubah.
CREATE OR REPLACE FUNCTION set_ceo_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_ceo_accounts_updated_at ON ceo_accounts;

CREATE TRIGGER trg_ceo_accounts_updated_at
BEFORE UPDATE ON ceo_accounts
FOR EACH ROW
EXECUTE FUNCTION set_ceo_updated_at();

-- Verifikasi schema.
SELECT id, username, is_active, created_at, updated_at
FROM ceo_accounts
ORDER BY id;
