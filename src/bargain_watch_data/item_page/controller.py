import logging as log
from dataclasses import dataclass
from typing import List, Optional

from selenium import webdriver

from bargain_watch_data.item_page.consts import ItemImageStatus
from bargain_watch_data.item_page.dataset import load_item_pages_history, save_item_page
from bargain_watch_data.item_page.models import ItemPage
from bargain_watch_data.item_page.scraper import get_item_page_images
from bargain_watch_data.lib.controller import BaseController

logger = log.getLogger()
logger.setLevel(log.INFO)


@dataclass(init=False)
class ItemPageController(BaseController):
    _driver: webdriver
    _item_pages_history: List[ItemPage]
    _item_page: Optional[ItemPage]

    def start(self):
        super().start()
        log.info("Starting WebDriver")
        self._item_pages_history = load_item_pages_history()
        log.info(f"Loading item pages history. Found {len(self._item_pages_history)} pages.")
        self._item_page = None

    def request(self, url: str):
        self._item_page = ItemPage(
            index=len(self._item_pages_history),
            url=url
        )
        log.info(f"Starting new request for url:\n{url}")
        _results = get_item_page_images(self._driver, url)
        log.info(f"Found {len(_results)} images.")
        self._item_page.images = _results

    def save(self):
        log.info("Saving item page.")
        save_item_page(self._item_page)

    @property
    def item_page(self) -> ItemPage:
        return self._item_page

    def set_image_status(self, index: int, value: ItemImageStatus):
        self._item_page.images[index].status = value

    def get_image_status(self, index: int):
        return self._item_page.images[index].status
