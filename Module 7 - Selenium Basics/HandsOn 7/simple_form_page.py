from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    """
    Page class for the Simple Form Demo page. Holds locators as class-level
    constants and provides action methods only - no assertions here.
    """

    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#showInput button")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        message_field = self.driver.find_element(*self.MESSAGE_INPUT)
        message_field.clear()
        message_field.send_keys(text)

    def click_submit(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_button.click()

    def get_displayed_message(self):
        displayed = self.wait_for_element(self.DISPLAYED_MESSAGE)
        return displayed.text
