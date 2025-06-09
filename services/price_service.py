from channels.coupang import CoupangPriceCrawler

class PriceService:    
    @staticmethod
    def get_price(channel, url):
        print("get_price")
        if channel == "coupang":
            crawler = CoupangPriceCrawler(headless=False)
            try:
                price = crawler.get_price(url)
            except Exception as e:
                print("Playwright 에러:", e)
                price = -1
            finally:
                crawler.quit()
            return price
        else:
            raise Exception("지원하지 않는 채널")

    @staticmethod
    def get_price_block(channel, url):
        if channel == "coupang":
            crawler = CoupangPriceCrawler(headless=False)
            try:
                price_block = crawler.get_price_block(url)
            except Exception as e:
                print("Playwright 에러:", e)
                price_block = None
            finally:
                crawler.quit()
            return price_block
        else:
            raise Exception("지원하지 않는 채널")