from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):
    """
    Page class for the Input Form Submit demo page.
    """

    NAME_FIELD = (By.NAME, "name")
    EMAIL_FIELD = (By.NAME, "email")
    PHONE_FIELD = (By.CSS_SELECTOR, "input[type='tel']")
    ADDRESS_FIELD = (By.NAME, "address")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg, .alert-success")

    def fill_form(self, name, email, phone, address):
        self.driver.find_element(*self.NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_FIELD).send_keys(address)

    def submit_form(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        message_element = self.wait_for_element(self.SUCCESS_MESSAGE)
        return message_element.text
