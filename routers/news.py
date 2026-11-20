import asyncio

from fastapi import APIRouter, Header, HTTPException, Query

from ..config import settings
from ..crawler import crawl_all
from ..database import CRAWL_LOG_TABLE, NEWS_TABLE, get_supabase
from ..feeds import CATEGORIES, FEEDS
from ..scheduler import next_run_time
from ..schemas import CategoryCount, News, NewsPage

router = APIRouter(prefix="/api", tags=["news"])

_background: set[asyncio.Task] = set()


@router.get("/categories", response_model=list[CategoryCount])
def list_categories():
    sb = get_supabase()
    out = []
    for name in CATEGORIES:
        res = sb.table(NEWS_TABLE).select("id", count="exact", head=True).eq("category", name).execute()
        out.append(CategoryCount(name=name, count=res.count or 0))
    return out


@router.get("/sources", response_model=list[str])
def list_sources():
    return sorted({s for s, _, _ in FEEDS})


@router.get("/news", response_model=NewsPage)
def list_news(
    category: str | None = Query(None, description="정치/경제/문화/사회/국제/지역/스포츠/IT과학"),
    source: str | None = Query(None, description="언론사명"),
    q: str | None = Query(None, max_length=100, description="제목 검색어"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    if category and category not in CATEGORIES:
        raise HTTPException(400, f"알 수 없는 카테고리: {category}")

    query = get_supabase().table(NEWS_TABLE).select("*", count="exact")
    if category:
        query = query.eq("category", category)
    if source:
        query = query.eq("source", source)
    if q and q.strip():
        query = query.ilike("title", f"%{q.strip()}%")

    start = (page - 1) * size
    res = (
        query.order("published_at", desc=True, nullsfirst=False)
        .order("id", desc=True)
        .range(start, start + size - 1)
        .execute()
    )
    return NewsPage(items=res.data or [], total=res.count or 0, page=page, size=size)


@router.get("/news/{news_id}", response_model=News)
def get_news(news_id: int):
    res = get_supabase().table(NEWS_TABLE).select("*").eq("id", news_id).limit(1).execute()
    if not res.data:
        raise HTTPException(404, "기사를 찾을 수 없습니다.")
    return res.data[0]


@router.get("/crawl/status")
def crawl_status():
    res = (
        get_supabase().table(CRAWL_LOG_TABLE)
        .select("*").order("started_at", desc=True).limit(1).execute()
    )
    return {"last_run": res.data[0] if res.data else None, "next_run": next_run_time()}


@router.post("/crawl", status_code=202)
async def trigger_crawl(x_admin_token: str | None = Header(None)):
    """수동 크롤링. ADMIN_TOKEN 이 설정돼 있으면 X-Admin-Token 헤더가 일치해야 한다."""
    if settings.admin_token and x_admin_token != settings.admin_token:
        raise HTTPException(401, "invalid admin token")
    task = asyncio.create_task(crawl_all())
    _background.add(task)
    task.add_done_callback(_background.discard)
    return {"status": "started"}
