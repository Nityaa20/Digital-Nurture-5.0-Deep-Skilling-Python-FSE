import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver(base_url):
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    drv.get(base_url)
    yield drv
    drv.quit()
