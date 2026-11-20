from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: int
    title: str
    link: str
    summary: str | None = None
    image_url: str | None = None
    source: str
    category: str
    published_at: datetime | None = None
    created_at: datetime


class NewsPage(BaseModel):
    items: list[News]
    total: int
    page: int
    size: int


class CategoryCount(BaseModel):
    name: str
    count: int
