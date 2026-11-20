from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    supabase_url: str = ""
    supabase_service_key: str = ""  # service_role 키 (서버 전용, 절대 프론트엔드에 노출 금지)

    crawl_interval_minutes: int = 60
    crawl_on_startup: bool = True
    request_timeout: float = 15.0
    user_agent: str = "Mozilla/5.0 (compatible; NewsCollector/1.0)"

    cors_origins: str = "http://localhost:5173"
    admin_token: str = ""  # 설정 시 POST /api/crawl 에 X-Admin-Token 헤더 필요

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
