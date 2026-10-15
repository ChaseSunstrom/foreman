---
name: selenium
title: Selenium
area: python
tags: [python, selenium, browser, testing, automation, webdriver]
detect: [dep:selenium, dep:pytest-selenium, dep:undetected-chromedriver]
related: [pytest, beautifulsoup, httpx, pytest-asyncio]
---
Selenium WebDriver 4: explicit waits, stable locators and a per-test browser lifecycle that is always quit.

## Verify
- `python -c "from selenium import webdriver; d=webdriver.Chrome(options=__import__('selenium.webdriver.chrome.options',fromlist=['Options']).Options()); d.quit()"`: Selenium Manager finds a driver and a browser starts.
- `pytest -q`: browser tests, headless in CI.
- `pytest -q -x --maxfail=1`: stop on first failure while diagnosing flakiness.
- `python -c "import selenium; print(selenium.__version__)"`: confirm the 4.x API.

## Test first
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()

def test_login_error_shown(driver, live_url):
    driver.get(f"{live_url}/login")
    driver.find_element(By.NAME, "email").send_keys("x@y.z")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    msg = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "error")))
    assert "password" in msg.text.lower()
```

## Do
- Use Selenium 4 style: `driver.find_element(By.CSS_SELECTOR, "...")` and `webdriver.Chrome(options=opts)`. Selenium Manager downloads the matching driver.
- Wait explicitly with `WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))`. Never rely on fixed sleeps.
- Prefer stable locators: `data-testid` attributes, ids, then CSS. Avoid long XPath chains.
- Use page objects: one class per page holding locators and actions, and keep assertions in tests.
- Quit the driver in fixture teardown (`driver.quit()`, not only `close()`).
- Run headless with `--headless=new`, set the window size (`--window-size=1280,800`) and keep one browser per test or per worker.
- Save a screenshot on failure with `driver.save_screenshot(path)` from a pytest hook.
- Seed test data through an API or fixtures, not through the UI each time.

## Avoid
- `time.sleep(n)`: slow and flaky. Use explicit waits.
- Mixing implicit and explicit waits: unpredictable timeouts. Use explicit only.
- The removed 3.x API: `find_element_by_id`, `executable_path=` and `desired_capabilities=`. Use `By` and `Options`/`Service`.
- Not quitting the browser on failure: zombie Chrome processes. Use a fixture with teardown.
- Reusing elements after navigation or re-render: `StaleElementReferenceException`. Re-find or wait for the new element.
- Parallel tests sharing one driver or profile: crossed state. One driver per worker.
- Using Selenium to scrape what an HTTP call returns: heavy. Use httpx.

## Review
- [ ] Every wait is explicit and bounded, with no sleeps.
- [ ] Locators use test ids or ids, not positions.
- [ ] Driver is quit on all paths and failures save a screenshot.
- [ ] Tests do not depend on each other's browser state.
