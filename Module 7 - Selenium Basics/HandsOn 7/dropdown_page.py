from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    """
    Page class for the Select Dropdown List demo page.
    """

    DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        dropdown_element = self.driver.find_element(*self.DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_visible_text(day_name)

    def get_selected_day(self):
        dropdown_element = self.driver.find_element(*self.DROPDOWN)
        select = Select(dropdown_element)
        return select.first_selected_option.text
