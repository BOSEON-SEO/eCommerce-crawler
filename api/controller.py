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
    
    result = PriceService.get_price(channel, url)
    return jsonify(result)

@bp.route('/api/price_block', methods=['POST'])
def get_price_block():
    data = request.get_json()
    channel = data.get('channel')
    url = data.get('url')
    if not channel or not url:
        return jsonify({"success": False, "error": "채널명과 상품 URL을 모두 입력하세요."}), 400
    
    result = PriceService.get_price_block(channel, url)
    return jsonify(result)