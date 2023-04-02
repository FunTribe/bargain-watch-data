import logging as log
from dataclasses import dataclass
from typing import List, Optional, Dict
from urllib.parse import urlparse

from bargain_watch_data.image_search.consts import ResultStatus
from bargain_watch_data.image_search.dataset import load_request_history, save_results, save_request
from bargain_watch_data.image_search.models import SearchRequest, SearchResult
from bargain_watch_data.image_search.scraper import get_search_results
from bargain_watch_data.lib.controller import BaseController
from bargain_watch_data.settings import URLBASE_WHITELIST

logger = log.getLogger()
logger.setLevel(log.INFO)


@dataclass(init=False)
class SearchController(BaseController):
    _requests_history: List[SearchRequest]
    _request: Optional[SearchRequest]
    _results: Dict[int, SearchResult]

    def start(self):
        super().start()
        log.info("Starting WebDriver")
        self._requests_history = load_request_history()
        log.info(f"Loading requests history. Found {len(self._requests_history)} requests.")
        self._request = None
        self._results = {}

    def request(self, url: str):
        if not self._request:
            self._request = SearchRequest(index=len(self._requests_history))
        self._request.urls.append(url)

        log.info(f"Starting new request for url:\n{url}")
        _results = get_search_results(self._driver, url)
        log.info(f"Found {len(_results)} results.")
        for result in _whitelist_filter_results(_results):
            result.index = len(self._results)
            self._results[result.index] = result

    @property
    def results(self):
        return self._results

    def set_result_status(self, index: int, value: ResultStatus):
        self._results[index].status = value

    def get_result_status(self, index: int):
        return self._results[index].status

    def save(self):
        log.info("Saving final results.")
        save_results(self._request, list(self._results.values()))
        save_request(self._request)


def _whitelist_filter_results(results: List[SearchResult]) -> List[SearchResult]:
    data = []
    for result in results:
        base_url = urlparse(result.url).netloc
        is_selected = base_url in URLBASE_WHITELIST
        decision_text = "ACCEPT" if is_selected else "SKIPPED"
        log.info(f"\tResult found on: {base_url} - {decision_text}")
        if is_selected:
            data.append(result)
    log.info(f"Selected {len(data)} final results.")
    return data
