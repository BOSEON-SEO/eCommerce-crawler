from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from core.base_crawler import BaseCrawler

class CoupangPriceCrawler(BaseCrawler):
    """
    쿠팡 상품 가격 추출 (Playwright + BeautifulSoup)
    """
    def __init__(self, headless=True, user_agent=None):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            user_agent=user_agent or UserAgent().random,
            locale="ko-KR"
        )
        self.page = self.context.new_page()

    # 가격 selctor 경우의 수가 너무 많음 -> 이거 잘 안쓸 듯
    def get_price(self, product_url):
        try:
            self.page.goto(product_url, wait_until="networkidle", timeout=5000)
        except Exception as e:
            print("페이지 로딩 실패:", e)
            return -1

        html = self.page.content()
        soup = BeautifulSoup(html, "html.parser")
        selectors = [
            ".prod-price-container .prod-price .prod-sale-price .total-price strong",
            ".prod-price-container .prod-price .prod-origin-price .origin-price",
            "main div.price-container div.final-price div.price-amount"
        ]

        price = None
        for selector in selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price = price_tag.get_text(strip=True)
                break

        if not price:
            price = -1
        return price
    
    # 대신 그냥 html 자체 가져와서 경우에 따라 python 혹은 js에서...
    def get_price_block(self, product_url):
        try:
            self.page.goto(product_url, wait_until="networkidle", timeout=5000)
        except Exception as e:
            print("페이지 로딩 실패:", e)
            return None
        
        html = self.page.content()
        soup = BeautifulSoup(html, "html.parser")
        selector = ".prod-price-container > .prod-price"

        price_block = soup.select_one(selector)
        if price_block:
            return str(price_block)
        else:
            return None

    def quit(self):
        self.browser.close()
        self.p.stop()
