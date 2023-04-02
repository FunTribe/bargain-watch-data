from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from bargain_watch_data.image_search.models import SearchResult


def _search_image_by_url(driver: webdriver, url: str) -> List[WebElement]:
    url = f"https://lens.google.com/uploadbyurl?url={url}"

    # load `url`
    driver.get(url)

    # check if we need to accept conditions
    if element := driver.find_elements(
        By.XPATH, "//*[contains(text(), 'Accept all')]"
    ):
        element[1].click()

    # scrap all results
    matches_header_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Visual matches')]")
    root_element = matches_header_element.find_element(By.XPATH, "../../div[2]/div/div/div")
    return root_element.find_elements(By.XPATH, ".//a")


def _parse_search_results(results: List[WebElement]) -> List[SearchResult]:

    def _parse_result(result: WebElement) -> SearchResult:
        url = result.get_attribute('href')
        result_content = result.find_element(By.XPATH, "./div")
        title = result_content.get_attribute("data-item-title")
        thumbnail_url = result_content.get_attribute("data-thumbnail-url")
        return SearchResult(
            url=url,
            title=title,
            thumbnail_url=thumbnail_url
        )
    return [
        _parse_result(result)
        for result in results
    ]


def get_search_results(driver: webdriver, url: str) -> List[SearchResult]:
    results = _search_image_by_url(driver, url)
    return _parse_search_results(results)

