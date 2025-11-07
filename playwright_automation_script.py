# No local imports—straight to the real deal
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://community.socialeagle.ai/')  # Test form for office-like automation
    page.fill('input[type="email"], input[name="email"]', 'hariprasanthmadhavan@socialeagle.ai')  # Replace with real email

    # page.click('button[type="submit"]')  # Or selector for sign-in button
    page.wait_for_selector('button[type="submit"], input[type="submit"]', timeout=5000)
    page.click('button[type="submit"], input[type="submit"]')
    
    # Wait for post-submit change (e.g., password field or error)
    page.wait_for_timeout(2000)  # 2s pause to observe
    print(f"Submit clicked! Current page URL: {page.url}")
    print(f"Page title after submit: {page.title()}")
    browser.close()
