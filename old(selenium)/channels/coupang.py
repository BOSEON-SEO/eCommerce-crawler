from core.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
from fake_useragent import UserAgent

class CoupangPriceCrawler(BaseCrawler):
    def __init__(self, user_agent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or UserAgent().random,
            "Accept-Language": "ko-KR,ko;q=0.9",
            "Referer": "https://www.coupang.com/",
        })
    
    """
    상품 가격 추출 - requests + bs4
    """
    def get_price(self, product_url):
        try:
            resp = self.session.get(product_url, timeout=5, headers=self.session.headers)
            print(resp.text)
        except requests.exceptions.Timeout:
            print("요청 타임아웃 발생")
            return -1
        except Exception as e:
            print("기타 에러:", e)
            return -1
        
        resp.raise_for_status()
        if resp.status_code != 200:
            return -1
        
        soup = BeautifulSoup(resp.text, 'html.parser')

        selectors = [
            ".prod-price-container .prod-price .prod-sale-price .total-price strong",
            ".prod-price-container .prod-price .prod-origin-price .origin-price",
            ".price-container .final-price .price-amount"
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

    """
    상품 가격 추출 - 웹드라이버
    """
    def get_price_with_webdriver(self, product_url):
        # 상품 페이지 진입
        self.get(product_url)

        # 쿠팡 가격 관련 selector 후보들
        selectors = [
            ".prod-price-container .prod-price .prod-sale-price .total-price strong",      # 1. 할인가 (js 미동작 시)
            ".prod-price-container .prod-price .prod-origin-price .origin-price",          # 2. 원가 (js 미동작 시)
            "main div.price-container div.final-price div.price-amount"                    # 3. 최종가 (js 동작 시)
        ]

        price = None

        html = None  # soup 재사용 방지
        for selector in selectors:
            # Selector 요소 대기
            try:
                self.wait_until(By.CSS_SELECTOR, selector, timeout=1)
            except Exception:
                pass

            # 매번 최신 페이지 소스 가져오기 (동적 렌더링 대응)
            html = self.get_page_source()
            soup = BeautifulSoup(html, 'html.parser')

            # 가격 파싱
            price_tag = soup.select_one(selector)
            if price_tag:
                price = price_tag.get_text(strip=True)
                break

        # 예외처리: 가격 태그 못 찾을 경우
        if not price:
            price = -1
        return price
