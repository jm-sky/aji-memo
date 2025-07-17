from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/ajimemo"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Security
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Cache TTL (in seconds)
    cache_ttl_default: int = 86400  # 1 day
    cache_ttl_bank_accounts: int = 604800  # 7 days

    # Rate limiting
    rate_limit_free_tier: int = 5  # requests per hour
    rate_limit_premium_tier: int = 1000  # requests per hour

    # CORS settings
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "GET,POST,PUT,DELETE,OPTIONS"
    cors_allow_headers: str = "*"

    # Admin user settings
    admin_name: str = "Admin"
    admin_email: str = "admin@ajimemo.com"
    admin_password: str = "admin123"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
