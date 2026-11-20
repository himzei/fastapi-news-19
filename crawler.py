"""RSS 크롤러: 피드를 병렬로 가져와 파싱한 뒤 Supabase 에 저장한다."""

import asyncio
import html
import logging
import re
from calendar import timegm
from datetime import datetime, timezone

import feedparser
import httpx

from .config import settings
from .database import CRAWL_LOG_TABLE, NEWS_TABLE, get_supabase
from .feeds import FEEDS

log = logging.getLogger("crawler")

MAX_CONCURRENCY = 8
UPSERT_CHUNK = 500
SUMMARY_MAX = 300

_TAG_RE = re.compile(r"<[^>]+>")
_IMG_RE = re.compile(r"""<img[^>]+src=["']([^"']+)["']""", re.I)
_WS_RE = re.compile(r"\s+")

# 수동 실행과 스케줄 실행이 겹치지 않도록
_crawl_lock = asyncio.Lock()


def _clean_text(raw: str | None) -> str:
    if not raw:
        return ""
    text = html.unescape(_TAG_RE.sub(" ", raw))
    return _WS_RE.sub(" ", text).strip()


def _extract_image(entry) -> str | None:
    for key in ("media_content", "media_thumbnail"):
        for m in entry.get(key) or []:
            if m.get("url"):
                return m["url"]
    for enc in entry.get("enclosures") or []:
        if (enc.get("type") or "").startswith("image") and enc.get("href"):
            return enc["href"]
    candidates = [entry.get("summary") or ""]
    candidates += [c.get("value", "") for c in entry.get("content") or []]
    for raw in candidates:
        m = _IMG_RE.search(raw)
        if m:
            return html.unescape(m.group(1))
    return None


def _published_at(entry) -> str:
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return datetime.fromtimestamp(timegm(t), tz=timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()


def parse_feed(content: bytes, source: str, category: str) -> list[dict]:
    parsed = feedparser.parse(content)
    items = []
    for entry in parsed.entries:
        link = (entry.get("link") or "").strip()
        title = _clean_text(entry.get("title"))
        if not link or not title:
            continue
        summary = _clean_text(entry.get("summary") or entry.get("description"))
        if len(summary) > SUMMARY_MAX:
            summary = summary[:SUMMARY_MAX].rstrip() + "…"
        items.append(
            {
                "title": title,
                "link": link,
                "summary": summary or None,
                "image_url": _extract_image(entry),
                "source": source,
                "category": category,
                "published_at": _published_at(entry),
            }
        )
    return items


async def _fetch_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, source: str, category: str, url: str):
    async with sem:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return parse_feed(resp.content, source, category), None
        except Exception as e:  # noqa: BLE001 - 피드 하나 실패해도 나머지는 계속
            log.warning("feed failed: %s %s %s (%s)", source, category, url, e)
            return [], {"source": source, "category": category, "url": url, "error": str(e)[:200]}


def _save(items: list[dict]) -> int:
    """link 기준으로 중복은 무시하고 새 기사만 저장. 새로 저장된 개수를 반환."""
    sb = get_supabase()
    inserted = 0
    for i in range(0, len(items), UPSERT_CHUNK):
        chunk = items[i : i + UPSERT_CHUNK]
        res = (
            sb.table(NEWS_TABLE)
            .upsert(chunk, on_conflict="link", ignore_duplicates=True)
            .execute()
        )
        inserted += len(res.data or [])
    return inserted


def _write_log(row: dict) -> None:
    try:
        get_supabase().table(CRAWL_LOG_TABLE).insert(row).execute()
    except Exception as e:  # noqa: BLE001
        log.warning("crawl log write failed: %s", e)


async def crawl_all() -> dict:
    if _crawl_lock.locked():
        log.info("crawl already running, skipped")
        return {"skipped": True}

    async with _crawl_lock:
        started = datetime.now(timezone.utc)
        sem = asyncio.Semaphore(MAX_CONCURRENCY)
        async with httpx.AsyncClient(
            timeout=settings.request_timeout,
            headers={"User-Agent": settings.user_agent},
            follow_redirects=True,
        ) as client:
            results = await asyncio.gather(
                *(_fetch_one(client, sem, s, c, u) for s, c, u in FEEDS)
            )

        # 같은 링크가 여러 피드에 있을 경우 먼저 나온 것만 사용
        seen: set[str] = set()
        items: list[dict] = []
        errors: list[dict] = []
        for feed_items, err in results:
            if err:
                errors.append(err)
            for it in feed_items:
                if it["link"] not in seen:
                    seen.add(it["link"])
                    items.append(it)

        inserted = 0
        if items:
            try:
                inserted = await asyncio.to_thread(_save, items)
            except Exception as e:  # noqa: BLE001
                log.error("DB save failed: %s", e)
                errors.append({"stage": "save", "error": str(e)[:200]})
        finished = datetime.now(timezone.utc)

        summary = {
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "fetched": len(items),
            "inserted": inserted,
            "errors": errors,
        }
        await asyncio.to_thread(_write_log, summary)
        log.info(
            "crawl done: fetched=%d inserted=%d errors=%d (%.1fs)",
            len(items), inserted, len(errors), (finished - started).total_seconds(),
        )
        return summary
