from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class Helper:
    driver: webdriver

    def mark(self, element: WebElement):
        self.driver.execute_script("arguments[0].style.backgroundColor = 'lightblue';", element)

    def unmark(self, element: WebElement):
        self.driver.execute_script("arguments[0].style.backgroundColor = 'white';", element)

    def hide(self, element: WebElement):
        self.driver.execute_script("arguments[0].style.display = 'none';", element)
