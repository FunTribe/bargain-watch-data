from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By

from bargain_watch_data.item_page.models import ItemImage


def get_item_page_images(driver: webdriver, url: str) -> Dict[int, ItemImage]:
    driver.get(url)
    gallery_root = driver.find_element(By.XPATH, "//*[@aria-label='Galeria produktu']")

    results = {}
    for img_element in gallery_root.find_elements(By.XPATH, ".//img"):
        img_url = img_element.get_attribute('src').split('?')[0] + "?imwidth=156"
        if "PREVIEW_IMG" in img_url:
            continue

        image = ItemImage(
            index=len(results),
            url=img_url
        )
        results[image.index] = image
    return results
