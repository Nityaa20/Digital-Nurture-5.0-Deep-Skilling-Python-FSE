# Hands-On 7 — Page Object Model

## Running the suite

```
pip install -r requirements.txt --break-system-packages
pytest tests/ -v --html=report.html --self-contained-html
```

## Why POM matters — maintenance scenario

Suppose the Submit button's `id` on the Simple Form Demo page changed from
`submit` to `btn-submit`.

**In a flat (non-POM) script:** every test file that directly calls
`driver.find_element(By.ID, "submit")` would break at the same time. If
that locator was copy-pasted into 10 different test files, you'd have to
find and fix it in all 10 places, and it's easy to miss one.

**With POM:** the locator lives in exactly one place — the
`SUBMIT_BUTTON` constant inside `SimpleFormPage`. Updating that single
line fixes every test that uses `click_submit()`, since they all go
through the page class rather than calling `find_element` directly. Test
files never contain locators or `find_element` calls at all — only calls
to page methods and assertions on their return values.
