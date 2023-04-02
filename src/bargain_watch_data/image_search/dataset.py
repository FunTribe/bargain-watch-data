import json
from dataclasses import asdict
from typing import List

from bargain_watch_data.image_search.models import SearchRequest, SearchResult
from bargain_watch_data.settings import REQUESTS_HISTORY_PATH, OUTPUT_DIR


def load_request_history() -> List[SearchRequest]:
    if REQUESTS_HISTORY_PATH.exists():
        return [
            SearchRequest(**json.loads(row))
            for row in open(REQUESTS_HISTORY_PATH).read().split('\n')
            if row
        ]
    return []


def save_request(request):
    with open(REQUESTS_HISTORY_PATH, "a") as output:
        output.write(json.dumps(asdict(request)) + "\n")


def save_results(request: SearchRequest, results: List[SearchResult]):
    with open(OUTPUT_DIR / f"{request.index}.jsonl", "w") as output:
        for row in results:
            output.write(json.dumps(asdict(row)) + "\n")
