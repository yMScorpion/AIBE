"""Well-known Vault secret paths for the AIBE system.

Centralises all paths to prevent typos and ensure consistency.
"""

from __future__ import annotations

# ── LLM APIs ──────────────────────────────────────────────────
VAULT_OPENROUTER_API_KEY = "llm/openrouter/api-key"
VAULT_ANTHROPIC_API_KEY = "llm/anthropic/api-key"
VAULT_OPENAI_API_KEY = "llm/openai/api-key"

# ── Infrastructure ────────────────────────────────────────────
VAULT_DATABASE_URL = "infra/database/url"
VAULT_REDIS_URL = "infra/redis/url"
VAULT_NATS_CREDENTIALS = "infra/nats/credentials"
VAULT_CLICKHOUSE_PASSWORD = "infra/clickhouse/password"

# ── Cloud providers ───────────────────────────────────────────
VAULT_AWS_ACCESS_KEY = "cloud/aws/access-key"
VAULT_VERCEL_TOKEN = "cloud/vercel/token"
VAULT_CLOUDFLARE_TOKEN = "cloud/cloudflare/token"

# ── Third-party services ─────────────────────────────────────
VAULT_RESEND_API_KEY = "services/resend/api-key"
VAULT_STRIPE_SECRET_KEY = "services/stripe/secret-key"
VAULT_TWILIO_AUTH_TOKEN = "services/twilio/auth-token"
VAULT_CALENDLY_API_KEY = "services/calendly/api-key"
VAULT_HUBSPOT_API_KEY = "services/hubspot/api-key"
VAULT_INTERCOM_API_KEY = "services/intercom/api-key"

# ── Social media ──────────────────────────────────────────────
VAULT_TWITTER_BEARER_TOKEN = "social/twitter/bearer-token"
VAULT_INSTAGRAM_ACCESS_TOKEN = "social/instagram/access-token"
VAULT_TIKTOK_ACCESS_TOKEN = "social/tiktok/access-token"
VAULT_LINKEDIN_ACCESS_TOKEN = "social/linkedin/access-token"

# ── Ads platforms ─────────────────────────────────────────────
VAULT_META_ADS_ACCESS_TOKEN = "ads/meta/access-token"
VAULT_GOOGLE_ADS_DEVELOPER_TOKEN = "ads/google/developer-token"

# ── Content generation ────────────────────────────────────────
VAULT_DALLE3_API_KEY = "content/dalle3/api-key"
VAULT_STABILITY_API_KEY = "content/stability/api-key"
VAULT_ELEVENLABS_API_KEY = "content/elevenlabs/api-key"
VAULT_RUNWAY_API_KEY = "content/runway/api-key"

# ── Security tools ────────────────────────────────────────────
VAULT_SNYK_TOKEN = "security/snyk/token"
VAULT_SHODAN_API_KEY = "security/shodan/api-key"
VAULT_NVD_API_KEY = "security/nvd/api-key"

# ── ML infrastructure ────────────────────────────────────────
VAULT_MODAL_TOKEN = "ml/modal/token"
VAULT_WANDB_API_KEY = "ml/wandb/api-key"
VAULT_HUGGINGFACE_TOKEN = "ml/huggingface/token"

# ── Research ──────────────────────────────────────────────────
VAULT_EXA_API_KEY = "research/exa/api-key"
VAULT_SERPAPI_KEY = "research/serpapi/api-key"
VAULT_JINA_API_KEY = "research/jina/api-key"

# ── Signing keys ─────────────────────────────────────────────
VAULT_HMAC_SIGNING_KEY = "internal/hmac/signing-key"
VAULT_JWT_SECRET_KEY = "internal/jwt/secret-key"

# ── OpenViking ────────────────────────────────────────────────
VAULT_OPENVIKING_API_KEY = "memory/openviking/api-key"
VAULT_OPENVIKING_CONNECTION = "memory/openviking/connection-string"


__all__ = [
    "VAULT_ANTHROPIC_API_KEY",
    "VAULT_AWS_ACCESS_KEY",
    "VAULT_CALENDLY_API_KEY",
    "VAULT_CLICKHOUSE_PASSWORD",
    "VAULT_CLOUDFLARE_TOKEN",
    "VAULT_DALLE3_API_KEY",
    "VAULT_DATABASE_URL",
    "VAULT_ELEVENLABS_API_KEY",
    "VAULT_EXA_API_KEY",
    "VAULT_GOOGLE_ADS_DEVELOPER_TOKEN",
    "VAULT_HMAC_SIGNING_KEY",
    "VAULT_HUBSPOT_API_KEY",
    "VAULT_HUGGINGFACE_TOKEN",
    "VAULT_INSTAGRAM_ACCESS_TOKEN",
    "VAULT_INTERCOM_API_KEY",
    "VAULT_JINA_API_KEY",
    "VAULT_JWT_SECRET_KEY",
    "VAULT_LINKEDIN_ACCESS_TOKEN",
    "VAULT_META_ADS_ACCESS_TOKEN",
    "VAULT_MODAL_TOKEN",
    "VAULT_NATS_CREDENTIALS",
    "VAULT_NVD_API_KEY",
    "VAULT_OPENAI_API_KEY",
    "VAULT_OPENROUTER_API_KEY",
    "VAULT_OPENVIKING_API_KEY",
    "VAULT_OPENVIKING_CONNECTION",
    "VAULT_REDIS_URL",
    "VAULT_RESEND_API_KEY",
    "VAULT_RUNWAY_API_KEY",
    "VAULT_SERPAPI_KEY",
    "VAULT_SHODAN_API_KEY",
    "VAULT_SNYK_TOKEN",
    "VAULT_STABILITY_API_KEY",
    "VAULT_STRIPE_SECRET_KEY",
    "VAULT_TIKTOK_ACCESS_TOKEN",
    "VAULT_TWITTER_BEARER_TOKEN",
    "VAULT_TWILIO_AUTH_TOKEN",
    "VAULT_VERCEL_TOKEN",
    "VAULT_WANDB_API_KEY",
]
