from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://www.lambdatest.com/selenium-playground/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# Task 1

# ---------------------------------------------------------------
# Locating the message input field on Simple Form Demo using
# all the different locator strategies
# ---------------------------------------------------------------
link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
link.click()

# By ID - the input field has id="user-message" on this page
el_by_id = driver.find_element(By.ID, "user-message")
print("found by ID:", el_by_id.is_displayed())

# By NAME - same field also has a name attribute
el_by_name = driver.find_element(By.NAME, "message")
print("found by NAME:", el_by_name.is_displayed())

# By CLASS_NAME - using the css class applied to the field
el_by_class = driver.find_element(By.CLASS_NAME, "form-control")
print("found by CLASS_NAME:", el_by_class.is_displayed())

# By TAG_NAME - just locating the first <input> tag on the page
el_by_tag = driver.find_element(By.TAG_NAME, "input")
print("found by TAG_NAME:", el_by_tag.is_displayed())

# By XPATH - absolute path (fragile, breaks if page structure changes)
el_by_xpath_absolute = driver.find_element(
    By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/div[1]/div/div[1]/input"
)
print("found by absolute XPATH:", el_by_xpath_absolute.is_displayed())

# By XPATH - relative path using attributes (more stable than absolute)
el_by_xpath_relative = driver.find_element(By.XPATH, "//input[@id='user-message']")
print("found by relative XPATH:", el_by_xpath_relative.is_displayed())


# ---------------------------------------------------------------
# Locating the same element using CSS selectors, 3 different ways
# ---------------------------------------------------------------
# by ID
css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
print("css by id:", css_by_id.is_displayed())

# by attribute
css_by_attribute = driver.find_element(By.CSS_SELECTOR, "[name='message']")
print("css by attribute:", css_by_attribute.is_displayed())

# by parent > child relationship
css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
print("css by parent-child:", css_by_parent_child.is_displayed())


# ---------------------------------------------------------------
# Checkbox Demo - using XPath with text() and contains()
# ---------------------------------------------------------------
driver.get(url)
checkbox_link = driver.find_element(By.LINK_TEXT, "Checkbox Demo")
checkbox_link.click()

# exact match using text()
option_1_label = driver.find_element(By.XPATH, "//label[text()='Option 1']")
print("Option 1 label found:", option_1_label.text)

# partial match using contains(), this finds all labels with "Option" in them
all_option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
print("total option labels found:", len(all_option_labels))
for label in all_option_labels:
    print(" -", label.text)


# ---------------------------------------------------------------
# Ranking the 6 locator strategies, most to least preferred
# ---------------------------------------------------------------
# 1. ID - best option, IDs are supposed to be unique on a page, and they
#    are short, fast, and readable. Least likely to change often.
#
# 2. CSS_SELECTOR - very fast, supported natively by browsers, and
#    readable. Can express almost anything except a few things like
#    "select by visible text" which XPath can do easily.
#
# 3. NAME - usually stable for form fields since backend/form processing
#    often depends on the name attribute, so it doesn't change often.
#
# 4. XPATH (relative, using attributes) - flexible, can traverse up/down
#    the DOM and match by text, but slightly slower than CSS and can get
#    complicated to read.
#
# 5. CLASS_NAME - risky because the same class is often reused on many
#    elements for styling purposes, and class names can change often
#    when the UI is redesigned.
#
# 6. TAG_NAME - least preferred, since tag names like "input" or "div"
#    are extremely generic and match many elements on a page, so it's
#    rarely unique and rarely useful on its own.
#
# XPATH with absolute path (starting from /html/body/...) is actually the
# worst of all, even worse than tag name, because it depends on the exact
# structure of the whole page. If even one div is added or removed
# anywhere above our element, the entire path breaks.


# Task 2

# ---------------------------------------------------------------
# Bootstrap Alerts - using WebDriverWait and ExpectedConditions
# ---------------------------------------------------------------
driver.get(url)
alerts_link = driver.find_element(By.LINK_TEXT, "Bootstrap Alerts")
alerts_link.click()

success_button = driver.find_element(By.XPATH, "//button[text()='Success Message']")
success_button.click()

# wait until the success alert div actually becomes visible before we try
# to read its text, instead of just hoping it's already there
success_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
)
assert "successfully" in success_alert.text
print("alert text:", success_alert.text)


# ---------------------------------------------------------------
# Comparing time.sleep() vs explicit wait
# ---------------------------------------------------------------
# version using time.sleep() - bad practice
driver.get(url)
alerts_link = driver.find_element(By.LINK_TEXT, "Bootstrap Alerts")
alerts_link.click()

start_sleep = time.time()
success_button = driver.find_element(By.XPATH, "//button[text()='Success Message']")
success_button.click()
time.sleep(3)  # just waits blindly for 3 seconds no matter what
alert_sleep_version = driver.find_element(By.CSS_SELECTOR, ".alert-success")
end_sleep = time.time()
print("time.sleep version took:", end_sleep - start_sleep, "seconds")

# version using explicit wait - good practice
driver.get(url)
alerts_link = driver.find_element(By.LINK_TEXT, "Bootstrap Alerts")
alerts_link.click()

start_wait = time.time()
success_button = driver.find_element(By.XPATH, "//button[text()='Success Message']")
success_button.click()
alert_wait_version = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
)
end_wait = time.time()
print("explicit wait version took:", end_wait - start_wait, "seconds")

# time.sleep(3) always waits the full 3 seconds no matter what, even if
# the alert appeared in half a second, which wastes time. explicit wait
# only waits as long as it actually needs to, so on a fast machine it
# finishes almost immediately, and on a slow machine it still waits up to
# the full timeout instead of failing too early like a short sleep would.
# so explicit wait is both faster on good days and safer on bad days.


# ---------------------------------------------------------------
# Waiting for element to be clickable before clicking it
# ---------------------------------------------------------------
driver.get(url)
alerts_link = driver.find_element(By.LINK_TEXT, "Bootstrap Alerts")
alerts_link.click()

clickable_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Success Message']"))
)
clickable_button.click()

# visibility_of_element_located just checks that the element is present
# in the DOM AND visible on the screen, but it could still be disabled or
# covered by another element on top of it. element_to_be_clickable checks
# all of that PLUS that the element is enabled and not blocked by
# anything else, so clicking it will actually work. that's why we use
# element_to_be_clickable specifically before performing a click action.


# ---------------------------------------------------------------
# FluentWait - polling every 500ms, ignoring NoSuchElementException
# ---------------------------------------------------------------
from selenium.webdriver.support.wait import WebDriverWait as FluentWebDriverWait

driver.get(url)
table_link = driver.find_element(By.LINK_TEXT, "Table Sort Search")
table_link.click()

fluent_wait = FluentWebDriverWait(
    driver,
    timeout=10,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException],
)

table_row = fluent_wait.until(
    lambda d: d.find_element(By.XPATH, "//table//tbody/tr[1]")
)
print("first table row found:", table_row.text)

driver.quit()
