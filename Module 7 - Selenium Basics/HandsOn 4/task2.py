from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.lambdatest.com/selenium-playground/"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)


# Navigate to Simple Form Demo, assert URL, navigate back

link = driver.find_element("link text", "Simple Form Demo")
link.click()

# check that we actually landed on the correct page by checking the URL contains the expected text
assert "simple-form-demo" in driver.current_url
print(driver.current_url)

# go back to the previous page, same as clicking the browser's back button
driver.back()
print(driver.current_url)


# Open a new tab, switch to it, print its title

# execute_script lets us run raw JavaScript in the browser. here we use it to open a new tab pointing to google
driver.execute_script('window.open("https://www.google.com");')

# every open tab/window has its own unique id, called a "handle". window_handles gives us the list of all these handles, in the order the
# tabs were opened. so handles[0] is our original tab and handles[1] is the new tab we just opened
tabs = driver.window_handles
print("number of tabs open:", len(tabs))

# selenium can only control one tab at a time, so we must explicitly tell it to switch to the new tab before we can interact with it
driver.switch_to.window(tabs[1])
print(driver.title)


# Switch back to original tab, take a screenshot

driver.switch_to.window(tabs[0])
print(driver.title)

# saves a screenshot of the current tab as a png file in the same folder
driver.save_screenshot("playground_screenshot.png")


# get_window_size() and set_window_size()

print(driver.get_window_size())

driver.set_window_size(1280, 800)
print(driver.get_window_size())


'''
 Why consistent window size matters for responsive UI automation:

 A lot of modern websites use responsive design, which means the layout of the page changes depending on how wide the browser window is. For
 example, a website might show a full navigation menu with all links visible when the window is wide, but on a smaller/narrower window it
 might hide that same menu behind a hamburger icon instead, or stack elements differently.

 If our automated tests run with different window sizes each time (for example, the default window size can be different on our local laptop
 vs a CI/CD server), an element we are trying to click might not even be visible in that particular layout, or it might load as a totally
 different element/structure on the page. This can make our test fail randomly, even though there is nothing actually wrong with the website
 the failure is only because the layout changed due to window size.

 By fixing the window size with set_window_size(), we make sure our test sees the exact same layout every single time it runs, no matter which
 machine it's running on. This makes our tests more reliable and reproducible.
'''

driver.quit()
