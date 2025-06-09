from flask import Blueprint, request, jsonify
from services.price_service import PriceService

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def index():
    return "Hello world"

@bp.route('/api/price', methods=['POST'])
def get_price():
    data = request.get_json()
    channel = data.get('channel')
    url = data.get('url')
    if not channel or not url:
        return jsonify({"success": False, "error": "채널명과 상품 URL을 모두 입력하세요."}), 400
    
    try:
        price = PriceService.get_price(channel, url)
        if price == -1:
            return jsonify({"success": False, "channel": channel, "url": url, "price": None, "error": "가격 정보를 찾을 수 없음"}), 200
        return jsonify({"success": True, "channel": channel, "url": url, "price": price})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/api/price_block', methods=['POST'])
def get_price_block():
    data = request.get_json()
    channel = data.get('channel')
    url = data.get('url')
    if not channel or not url:
        return jsonify({"success": False, "error": "채널명과 상품 URL을 모두 입력하세요."}), 400
    
    try:
        price_block = PriceService.get_price_block(channel, url)
        if price_block is None:
            return jsonify({"success": False, "channel": channel, "url": url, "price_block": None, "error": "가격 정보를 찾을 수 없음"}), 200
        return jsonify({"success": True, "channel": channel, "url": url, "price_block": price_block})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500