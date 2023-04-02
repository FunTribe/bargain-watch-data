from pathlib import Path

# Paths
DATA_DIR = Path("./data/")
DATA_DIR.mkdir(exist_ok=True, parents=True)

OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

REQUESTS_HISTORY_PATH = DATA_DIR / "requests.jsonl"

ITEM_PAGES_HISTORY_PATH = DATA_DIR / "item_pages.jsonl"

# Config
URLBASE_WHITELIST = [
    "www.zalando.pl",
    "modivo.pl",
    "answear.com",
    "www.asos.com",
    "www.aboutyou.pl",
    "www.peek-cloppenburg.pl"
]


LANGUAGE = "EN"
