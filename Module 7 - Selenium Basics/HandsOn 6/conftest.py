import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# this just stores the url in one place so we dont have to type it again
# and again in every test
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# this fixture opens the browser before a test runs and closes it after
# the test is done. scope="function" means it does this for every single
# test, so each test gets its own fresh browser
@pytest.fixture(scope="function")
def driver(base_url):
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    drv.get(base_url)

    # whatever is before yield runs first (this is the setup part)
    yield drv

    # whatever is after yield runs after the test finishes (this is the
    # teardown part), here we just close the browser
    drv.quit()


# this function runs automatically after every test, we dont call it
# ourselves. it checks if the test failed, and if it did, it takes a
# screenshot and saves it
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            test_name = item.name
            driver_fixture.save_screenshot(f"{test_name}_failure.png")
