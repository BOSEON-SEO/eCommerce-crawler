from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from fake_useragent import UserAgent
import time

class BaseCrawler:
    """
    Selenium 기반 크롤러의 공통 기능 제공 (모든 크롤러의 부모)
    - 드라이버 초기화, 옵션, 자원관리 등
    """

    def __init__(self, headless=True, implicit_wait=5, user_agent=None):
        # Selenium Chrome 드라이버를 초기화 (옵션: headless, User-Agent, 윈도우 사이즈 등)
        # options = webdriver.ChromeOptions()
        options = uc.ChromeOptions()
        
        # (1) headless 모드 (브라우저 창 안 띄움)
        if headless:
            options.add_argument('--headless=new')  # 최신 headless 모드
            options.add_argument('--disable-gpu')   # GPU 가속 off
            options.add_argument('--no-sandbox')    # 샌드박스 off
        
        # (2) 창 크기: 일반 사용자 환경 맞춤
        options.add_argument('--window-size=1280,1024')    # 창 크기

        # (3) 언어 설정: 한국어 브라우저 환경
        options.add_argument('--lang=ko-KR,ko')            # 언어

        # (4) User-Agent 지정
        ua = user_agent or UserAgent().random
        options.add_argument(f'--user-agent={ua}')    # UA 지정
        
        # (5) 자동화 탐지 우회
        options.add_argument('--disable-blink-features=AutomationControlled')  # Selenium 감지 우회

        # (6) 불필요한 브라우저 로그, 자동화 표시 숨김
        # options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        # options.add_experimental_option('useAutomationExtension', False)

        # 드라이버 실행
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(implicit_wait)

        # (7) 추가적 webdriver 감지 우회 (실행 후)
        try:
            # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    window.navigator.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko']});
                '''
            })
            
            stealth(
                self.driver,
                languages=["ko-KR", "ko"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
            )

            self.driver.execute_cdp_cmd(
                'Network.setExtraHTTPHeaders',
                {
                    'headers': {
                        'User-Agent': ua,
                        'Accept-Language': 'ko-KR,ko;q=0.9',
                        'Referer': 'https://www.coupang.com/',
                    }
                }
            )
        except Exception:
            pass

    def get(self, url):
         # 지정한 URL로 이동 (기본적으로 렌더링 대기)
        self.driver.get(url)
        time.sleep(1)

    def get_page_source(self):
        # 현재 브라우저의 전체 HTML 소스 반환
        return self.driver.page_source

    def wait_until(self, by, value, timeout=10):
        # 지정된 셀렉터(by, value)에 해당하는 element가 나타날 때까지 최대 timeout초 대기
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def scroll_to_bottom(self, step=500, delay=0.3, max_scrolls=50):
        # 페이지를 step 픽셀씩 아래로 스크롤하여 끝까지 이동 (리뷰 등 무한스크롤용)
        last_height = self.driver.execute_script('return document.body.scrollHeight')
        scrolls = 0
        while True:
            self.driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(delay)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height or scrolls >= max_scrolls:
                break
            last_height = new_height
            scrolls += 1

    def quit(self):
        # 드라이버 세션 종료 및 리소스 해제
        self.driver.quit()
