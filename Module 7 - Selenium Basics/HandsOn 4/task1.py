from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------
# Selenium Architecture - 3 main components
# ---------------------------------------------------------------

# WebDriver:
# WebDriver is the core part of Selenium that actually controls the
# browser. When we write commands in Python like driver.get() or
# element.click(), Selenium sends these commands to a browser-specific
# driver program (like chromedriver for Chrome, geckodriver for Firefox).
# This driver then talks directly to the browser using the browser's own
# native automation support (for example Chrome DevTools Protocol for
# Chrome). This is different from the old Selenium RC, which used to
# inject JavaScript into the browser - WebDriver controls the browser
# from outside, at the OS/process level, so it behaves more like a real
# user and can do things JavaScript injection could not do reliably, like
# handling browser popups, file uploads, and native alerts.

# Selenium Grid:
# Selenium Grid solves the problem of running tests on multiple machines,
# operating systems, and browsers at the same time. Normally, if we have
# 100 test cases and want to check them on Chrome, Firefox, and Edge, we
# would have to run them one browser after another, which takes a very
# long time. Grid has one central "hub" that receives test requests, and
# multiple "nodes" (which can be different machines with different
# browsers/OS installed) that actually execute the tests. The hub
# distributes the tests to available nodes so many tests run in parallel
# instead of one after another. This massively reduces total execution
# time and also gives real cross-browser/cross-platform coverage.

# Selenium IDE:
# Selenium IDE is a browser extension (available for Chrome and Firefox)
# used mainly for record-and-playback style test creation. We open our
# website, click around, fill forms, and interact normally, while
# Selenium IDE silently records each action we take (click, type, select,
# etc) as a step. These recorded steps can be replayed automatically
# later, without us doing it manually again. It can also export/generate
# the recorded steps into real code, like Python + Selenium WebDriver
# format, so it's useful for beginners to quickly get working test code,
# or for testers who don't want to write code from scratch for simple
# scenarios.

url = "https://www.lambdatest.com/selenium-playground/"


# ---------------------------------------------------------------
# Minimal script - open browser, go to page, print title, close
# ---------------------------------------------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
print(driver.title)
driver.quit()


# ---------------------------------------------------------------
# Same script but with implicit wait added
# ---------------------------------------------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# implicit wait tells the driver: whenever you try to find an element and
# it's not there yet, keep checking again and again for up to 10 seconds
# before giving up and throwing an error
driver.implicitly_wait(10)

driver.get(url)
print(driver.title)
driver.quit()

# Why implicit wait is considered bad practice compared to explicit wait:
#
# 1. It is set ONCE for the entire driver session and applies to EVERY
#    single find_element call in the script. We cannot make it wait
#    longer for one tricky element and shorter for an easy one - it's the
#    same fixed timeout everywhere.
#
# 2. It only checks whether the element EXISTS in the page's HTML (the
#    DOM). It does NOT check whether the element is visible on the
#    screen, or whether it is enabled/clickable. So an element can
#    "pass" the implicit wait check because it exists in the DOM, but the
#    test can still fail right after with an error like
#    ElementNotInteractableException, because the element was hidden or
#    disabled at that moment.
#
# 3. If an element never appears at all (for example due to a real bug),
#    the test has to wait out the FULL 10 seconds before it fails,
#    slowing down the whole test run unnecessarily.
#
# 4. Mixing implicit wait with explicit wait (WebDriverWait +
#    ExpectedConditions) in the same script can cause unpredictable
#    behaviour, since the two timers can add up in confusing ways.
#
# Because of these issues, explicit waits are preferred - they let us
# wait for a specific condition (like "element is visible" or "element
# is clickable") on a specific element only, which is both faster and
# more reliable. Explicit waits are covered in detail in Hands-On 5.


# ---------------------------------------------------------------
# Running the same script in headless mode
# ---------------------------------------------------------------
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# headless mode runs the browser in the background with no visible
# window on screen. this is commonly used when running tests on a server
# or in a CI/CD pipeline where there is no display/monitor attached, and
# it can also be slightly faster since the browser doesn't need to render
# anything visually. we can verify it still works correctly because the
# page title still prints correctly below, even without a browser window
# popping up
print(driver.title)
driver.quit()
