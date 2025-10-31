import base64
from io import BytesIO
import cv2
import numpy as np
import requests
from PIL import Image, ImageEnhance

def get_image_bytes(image_data):
    """将不同格式的图像数据转换为字节流"""
    if isinstance(image_data, bytes):
        return image_data
    elif image_data.startswith('http'):
        response = requests.get(image_data, verify=False)
        response.raise_for_status()
        return response.content
    elif isinstance(image_data, str):
        return base64.b64decode(image_data)
    else:
        raise ValueError("Unsupported image data type")

def preprocess_image(image_bytes, enhance=False, denoise=False, binarize=False):
    """图片预处理函数"""
    try:
        image = Image.open(BytesIO(image_bytes))
        
        if enhance:
            # 增强对比度
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            # 增强锐度
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
        
        # 转换为numpy数组用于OpenCV处理
        img_array = np.array(image)
        
        if denoise:
            # 去噪
            img_array = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        
        if binarize:
            # 转灰度
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            # 二值化
            _, img_array = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 转回bytes
        _, buffer = cv2.imencode('.png', img_array)
        return buffer.tobytes()
    except Exception as e:
        raise Exception(f"图片预处理错误: {e}")

def image_to_base64(image, format='PNG'):
    """将PIL图像转换为Base64字符串"""
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str
