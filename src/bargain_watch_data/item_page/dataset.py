from dataclasses import asdict
from typing import List
import json
from bargain_watch_data.item_page.models import ItemPage
from bargain_watch_data.settings import ITEM_PAGES_HISTORY_PATH


def load_item_pages_history() -> List[ItemPage]:
    if ITEM_PAGES_HISTORY_PATH.exists():
        return [
            ItemPage(**json.loads(row))
            for row in open(ITEM_PAGES_HISTORY_PATH).read().split('\n')
            if row
        ]
    return []


def save_item_page(item_page: ItemPage):
    with open(ITEM_PAGES_HISTORY_PATH, "a") as output:
        output.write(json.dumps(asdict(item_page)) + "\n")
