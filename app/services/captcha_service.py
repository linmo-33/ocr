import re
import base64
from io import BytesIO
import cv2
import numpy as np
import ddddocr
from PIL import Image
from flask import current_app

from app.utils.image_processor import get_image_bytes, preprocess_image, image_to_base64

class CaptchaService:
    """验证码识别服务"""
    
    def __init__(self):
        self.ocr = ddddocr.DdddOcr(show_ad=False)
        self.det = ddddocr.DdddOcr(det=True, show_ad=False)
    
    def slide_match(self, sliding_image, back_image, simple_target=True, preprocess=False):
        """滑块验证码识别"""
        try:
            sliding_bytes = get_image_bytes(sliding_image)
            back_bytes = get_image_bytes(back_image)
            
            if preprocess:
                sliding_bytes = preprocess_image(sliding_bytes, enhance=True)
                back_bytes = preprocess_image(back_bytes, enhance=True)
            
            res = self.ocr.slide_match(sliding_bytes, back_bytes, simple_target=simple_target)
            return {'position': res['target'][0], 'confidence': res.get('confidence', 0.95)}
        except Exception as e:
            current_app.logger.error(f"滑块识别错误: {e}")
            return None
    
    def slide_comparison(self, sliding_image, back_image):
        """滑块对比"""
        try:
            sliding_bytes = get_image_bytes(sliding_image)
            back_bytes = get_image_bytes(back_image)
            res = self.ocr.slide_comparison(sliding_bytes, back_bytes)
            return res['target'][0]
        except Exception as e:
            current_app.logger.error(f"滑块对比错误: {e}")
            return None
    
    def classify(self, image, preprocess=False):
        """OCR文字识别"""
        try:
            image_bytes = get_image_bytes(image)
            
            if preprocess:
                image_bytes = preprocess_image(image_bytes, enhance=True, denoise=True)
            
            res = self.ocr.classification(image_bytes)
            return {'text': res, 'confidence': 0.90}
        except Exception as e:
            current_app.logger.error(f"OCR识别错误: {e}")
            return None
    
    def batch_classify(self, images, preprocess=False):
        """批量OCR识别"""
        try:
            results = []
            for idx, image in enumerate(images):
                result = self.classify(image, preprocess)
                if result:
                    results.append({'index': idx, 'result': result})
                else:
                    results.append({'index': idx, 'error': '识别失败'})
            return results
        except Exception as e:
            current_app.logger.error(f"批量识别错误: {e}")
            return None
    
    def detect(self, image):
        """目标检测"""
        try:
            image_bytes = get_image_bytes(image)
            poses = self.det.detection(image_bytes)
            return poses
        except Exception as e:
            current_app.logger.error(f"检测错误: {e}")
            return None
    
    def calculate(self, image):
        """计算类验证码"""
        try:
            image_bytes = get_image_bytes(image)
            expression = self.ocr.classification(image_bytes)
            expression = re.sub('=.*', '', expression)
            expression = re.sub('[^0-9+\-*/()]', '', expression)
            result = eval(expression)
            return result
        except Exception as e:
            current_app.logger.error(f"计算验证码错误: {e}")
            return None
    
    def crop_image(self, image_url, y_coordinate):
        """图片分割"""
        try:
            import requests
            image = Image.open(BytesIO(requests.get(image_url).content))
            upper_half = image.crop((0, 0, image.width, y_coordinate))
            lower_half = image.crop((0, y_coordinate*2, image.width, image.height))
            
            return {
                'slidingImage': image_to_base64(upper_half),
                'backImage': image_to_base64(lower_half)
            }
        except Exception as e:
            current_app.logger.error(f"图片分割错误: {e}")
            return None
    
    def click_select(self, image):
        """点选验证码"""
        try:
            image_bytes = get_image_bytes(image)
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            im = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            bboxes = self.det.detection(image_bytes)
            
            results = []
            for bbox in bboxes:
                x1, y1, x2, y2 = map(int, bbox)
                cropped_image = im[y1:y2, x1:x2]
                _, buffer = cv2.imencode('.png', cropped_image)
                image_base64 = base64.b64encode(buffer).decode('utf-8')
                text = self.ocr.classification(image_base64)
                results.append({text: bbox.tolist()})
            
            return results
        except Exception as e:
            current_app.logger.error(f"点选识别错误: {e}")
            return None
