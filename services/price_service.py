from channels.coupang import CoupangPriceCrawler

class PriceService:
    @staticmethod
    def get_price(channel, url):
        if channel == "coupang":
            crawler = CoupangPriceCrawler()
            try:
                price = crawler.get_price(url)
                if price == -1:
                    return {"success": False, "error": "가격 정보를 찾을 수 없음"}
                return {"success": True, "price": price}
            except Exception as e:
                return {"success": False, "error": str(e)}
            finally:
                crawler.quit()
        else:
            return {"success": False, "error": "지원하지 않는 채널"}

    @staticmethod
    def get_price_block(channel, url):
        if channel == "coupang":
            crawler = CoupangPriceCrawler()
            try:
                price_block = crawler.get_price_block(url)
                if price_block is None:
                    return {"success": False, "error": "가격 정보를 찾을 수 없음"}
                return {"success": True, "price_block": price_block}
            except Exception as e:
                return {"success": False, "error": str(e)}
            finally:
                crawler.quit()
        else:
            return {"success": False, "error": "지원하지 않는 채널"}