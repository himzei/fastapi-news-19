from functools import lru_cache

from supabase import Client, create_client

from .config import settings

class SupabaseNotConfigured(RuntimeError):
    pass


NEWS_TABLE = "news"
CRAWL_LOG_TABLE = "crawl_logs"


@lru_cache
def get_supabase() -> Client:
    if not settings.supabase_url or not settings.supabase_service_key:
        raise SupabaseNotConfigured(
            "SUPABASE_URL / SUPABASE_SERVICE_KEY 가 설정되지 않았습니다. backend/.env 를 확인하세요."
        )
    return create_client(settings.supabase_url, settings.supabase_service_key)
