from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://naver.com")
    input("아무 글자나 입력시 종료")
    browser.close()
