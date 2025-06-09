import requests
from bs4 import BeautifulSoup

api_key = "c6ef64e5ca7064776d8f46384c170018"
target_url = "https://www.coupang.com/vp/products/8172100881"
api_url = f"http://api.scraperapi.com/?api_key={api_key}&url={target_url}&ultra_premium=true"

res = requests.get(api_url)
print(res.text)
soup = BeautifulSoup(res.text, "html.parser")
price = soup.select_one(".prod-price-container .prod-price")
print(price.text if price else "가격 정보 없음")
