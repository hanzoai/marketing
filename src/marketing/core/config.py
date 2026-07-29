"""Marketing service configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Marketing service settings."""

    # Service
    service_name: str = "hanzo-marketing"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8001

    # Hanzo Stack Integration
    datastore_url: str = "http://datastore:8123"
    datastore_db: str = "marketing"
    datastore_user: str = "hanzo"
    # No default. A credential with a working default is the one that reaches
    # production: it succeeds locally, nobody is prompted to set it, and the
    # value that ships is the one written here. These are supplied from KMS via
    # the environment, and pydantic refuses to construct Settings without them —
    # so a missing secret is a startup failure rather than a silent fallback to
    # a password that is published in this file.
    datastore_password: str

    router_url: str = "http://router:4000/v1"
    router_api_key: str

    analytics_url: str = "http://analytics:3000"

    # DSNs carry their own credential, so they are secrets whole.
    redis_url: str
    postgres_url: str
    nats_url: str = "nats://nats:4222"

    # Ad Platforms
    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_access_token: str = ""

    google_ads_developer_token: str = ""
    google_ads_client_id: str = ""
    google_ads_client_secret: str = ""
    google_ads_refresh_token: str = ""

    tiktok_app_id: str = ""
    tiktok_app_secret: str = ""
    tiktok_access_token: str = ""

    # Communication
    sendgrid_api_key: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Social
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_secret: str = ""

    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""

    # Optimizer
    optimizer_population_size: int = 50
    optimizer_generations: int = 100
    optimizer_mutation_rate: float = 0.1
    optimizer_crossover_rate: float = 0.7

    class Config:
        env_prefix = "MARKETING_"
        env_file = ".env"


settings = Settings()
