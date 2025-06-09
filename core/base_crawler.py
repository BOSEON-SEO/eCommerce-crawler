from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent

class BaseCrawler:
    def __init__(self, headless=False, user_agent=None):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            user_agent=user_agent or UserAgent().random,
            locale="ko-KR"
        )
        self.page = self.context.new_page()

    def get(self, url):
        self.page.goto(url, wait_until="networkidle")

    def get_page_source(self):
        return self.page.content()

    def wait_until(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, timeout=timeout)

    def scroll_to_bottom(self, step=500, delay=0.3, max_scrolls=50):
        # Playwright는 아래처럼 JS로 스크롤
        for _ in range(max_scrolls):
            self.page.evaluate(f"window.scrollBy(0, {step});")
            self.page.wait_for_timeout(int(delay * 1000))

    def quit(self):
        self.browser.close()
        self.p.stop()