from flask import request, jsonify, current_app
from app.routes import api_bp
from app import limiter
from app.utils.stats import track_stats
from app.services.captcha_service import CaptchaService

# 初始化服务
captcha_service = CaptchaService()

@api_bp.route('/capcode', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('capcode')
def capcode():
    """
    滑块验证码识别
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            slidingImage:
              type: string
            backImage:
              type: string
            simpleTarget:
              type: boolean
              default: true
            preprocess:
              type: boolean
              default: false
    responses:
      200:
        description: 识别结果
    """
    try:
        data = request.get_json()
        result = captcha_service.slide_match(
            data['slidingImage'],
            data['backImage'],
            data.get('simpleTarget', True),
            data.get('preprocess', False)
        )
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        current_app.logger.error(f"出现错误: {e}")
        return jsonify({'error': str(e)}), 400

@api_bp.route('/slideComparison', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('slideComparison')
def slide_comparison():
    """滑块对比识别"""
    try:
        data = request.get_json()
        result = captcha_service.slide_comparison(
            data['slidingImage'],
            data['backImage']
        )
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/classification', methods=['POST'])
@limiter.limit("50 per minute")
@track_stats('classification')
def classification():
    """OCR文字识别"""
    try:
        data = request.get_json()
        result = captcha_service.classify(
            data['image'],
            data.get('preprocess', False)
        )
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/batch/classification', methods=['POST'])
@limiter.limit("10 per minute")
@track_stats('batch_classification')
def batch_classification():
    """批量OCR文字识别"""
    try:
        data = request.get_json()
        images = data['images']
        
        if len(images) > current_app.config['MAX_BATCH_SIZE']:
            return jsonify({'error': f'单次最多处理{current_app.config["MAX_BATCH_SIZE"]}张图片'}), 400
        
        result = captcha_service.batch_classify(
            images,
            data.get('preprocess', False)
        )
        if result is None:
            return jsonify({'error': '批量处理过程中出现错误'}), 500
        return jsonify({'results': result, 'total': len(images)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/detection', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('detection')
def detection():
    """目标检测"""
    try:
        data = request.get_json()
        result = captcha_service.detect(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/calculate', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('calculate')
def calculate():
    """计算类验证码识别"""
    try:
        data = request.get_json()
        result = captcha_service.calculate(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/crop', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('crop')
def crop():
    """图片分割"""
    try:
        data = request.get_json()
        result = captcha_service.crop_image(
            data['image'],
            data['y_coordinate']
        )
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/select', methods=['POST'])
@limiter.limit("30 per minute")
@track_stats('select')
def select():
    """点选验证码识别"""
    try:
        data = request.get_json()
        result = captcha_service.click_select(data['image'])
        if result is None:
            return jsonify({'error': '处理过程中出现错误'}), 500
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
