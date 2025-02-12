import json
import os
import urllib

from playwright.sync_api import sync_playwright

capabilities = {
    'browserName': 'Chrome',  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 10',
        'build': 'Playwright Build',
        'name': 'Playwright Test',
        'user': os.getenv('LT_USERNAME'),
        'accessKey': os.getenv('LT_ACCESS_KEY'),
        'network': False,
        'video': True
    }
}


def run(playwright):
    lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(
        json.dumps(capabilities))
    iphone = playwright.devices["iPhone 11"]  # Documentation: https://playwright.dev/docs/emulation#devices
    browser = playwright.chromium.connect(lt_cdp_url)
    context = browser.new_context(**iphone)
    page = context.new_page()

    try:
        page.goto("https://www.bing.com/")
        page.fill("[aria-label='Enter your search term']", 'LambdaTest')
        page.keyboard.press("Enter")

        title = page.title()

        print("Title:: ", title)

        if "Lambdatest" not in title:
            set_test_status(page, "passed", "Title matched")
        else:
            set_test_status(page, "failed", "Title did not match")
    except Exception as err:
        print("Error:: ", err)
        set_test_status(page, "failed", str(err))

    browser.close()


def set_test_status(page, status, remark):
    page.evaluate("_ => {}",
                  "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");


with sync_playwright() as playwright:
    run(playwright)
