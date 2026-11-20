from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import settings
from .crawler import crawl_all

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")


def start_scheduler() -> None:
    scheduler.add_job(
        crawl_all,
        trigger="interval",
        minutes=settings.crawl_interval_minutes,
        id="rss_crawl",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        # 서버 시작 직후 1회 실행 후 매 주기마다 실행
        next_run_time=datetime.now(scheduler.timezone) if settings.crawl_on_startup else None,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


def next_run_time() -> str | None:
    job = scheduler.get_job("rss_crawl")
    return job.next_run_time.isoformat() if job and job.next_run_time else None
