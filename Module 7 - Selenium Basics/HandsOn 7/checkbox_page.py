from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    """
    Page class for the Checkbox Demo page.
    """

    def _checkbox_locator(self, index):
        # index is 1-based to match how the exercise refers to options
        return (By.XPATH, f"(//input[@type='checkbox'])[{index}]")

    def check_option(self, index):
        checkbox = self.driver.find_element(*self._checkbox_locator(index))
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index):
        checkbox = self.driver.find_element(*self._checkbox_locator(index))
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index):
        checkbox = self.driver.find_element(*self._checkbox_locator(index))
        return checkbox.is_selected()
