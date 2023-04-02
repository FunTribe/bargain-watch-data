from dataclasses import dataclass, field
from typing import Optional, List

from bargain_watch_data.image_search.consts import ResultStatus


@dataclass
class SearchResult:
    url: str
    title: str
    thumbnail_url: str
    status: Optional[ResultStatus] = field(default=ResultStatus.REJECT)
    index: Optional[int] = field(default=None)


@dataclass
class SearchRequest:
    index: int
    urls: List[str] = field(default_factory=list)
