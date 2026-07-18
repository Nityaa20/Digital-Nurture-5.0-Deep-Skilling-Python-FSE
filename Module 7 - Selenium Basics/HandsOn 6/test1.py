import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Task 1


def test_simple_form_submission(driver, base_url):
    driver.get(base_url)

    link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
    link.click()

    # type our message in the input box
    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys("Hello Selenium")

    submit_button = driver.find_element(By.CSS_SELECTOR, "#showInput button")
    submit_button.click()

    # wait for the message to actually show up on the page before we check it
    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    assert displayed_message.text == "Hello Selenium"


def test_checkbox_demo(driver, base_url):
    driver.get(base_url)

    link = driver.find_element(By.LINK_TEXT, "Checkbox Demo")
    link.click()

    first_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox'][1]")

    # click it once, it should get checked now
    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    # click it again, it should get unchecked now
    first_checkbox.click()
    assert first_checkbox.is_selected() is False


# Task 2


# this same test runs 3 times, once for each value in the list below,
# so we dont have to copy paste the same test 3 times
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission_parametrized(driver, base_url, message):
    driver.get(base_url)

    link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
    link.click()

    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys(message)

    submit_button = driver.find_element(By.CSS_SELECTOR, "#showInput button")
    submit_button.click()

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )

    assert displayed_message.text == message


def test_dropdown_selection(driver, base_url):
    driver.get(base_url)

    link = driver.find_element(By.LINK_TEXT, "Select Dropdown List")
    link.click()

    dropdown_element = driver.find_element(By.ID, "select-demo")

    # Select is a helper class made for handling normal html dropdowns,
    # its better than just clicking the option directly
    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Wednesday")

    selected_option = dropdown.first_selected_option
    assert selected_option.text == "Wednesday"


# this test is written to fail on purpose, just so we can see the
# screenshot on failure hook (in conftest.py) actually working when we
# run the suite. remove this test before final submission
def test_intentional_failure_for_screenshot_demo(driver, base_url):
    driver.get(base_url)
    assert "some-text-that-does-not-exist" in driver.title
