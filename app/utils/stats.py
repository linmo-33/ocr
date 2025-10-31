import time
from functools import wraps
from flask import current_app

# 统计数据
stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'total_processing_time': 0,
    'endpoints': {}
}

def track_stats(endpoint_name):
    """统计装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            stats['total_requests'] += 1
            
            if endpoint_name not in stats['endpoints']:
                stats['endpoints'][endpoint_name] = {
                    'count': 0,
                    'success': 0,
                    'failed': 0,
                    'avg_time': 0
                }
            
            stats['endpoints'][endpoint_name]['count'] += 1
            
            try:
                result = f(*args, **kwargs)
                stats['successful_requests'] += 1
                stats['endpoints'][endpoint_name]['success'] += 1
                return result
            except Exception as e:
                stats['failed_requests'] += 1
                stats['endpoints'][endpoint_name]['failed'] += 1
                raise e
            finally:
                processing_time = time.time() - start_time
                stats['total_processing_time'] += processing_time
                endpoint_stats = stats['endpoints'][endpoint_name]
                endpoint_stats['avg_time'] = (
                    (endpoint_stats['avg_time'] * (endpoint_stats['count'] - 1) + processing_time) 
                    / endpoint_stats['count']
                )
        return wrapper
    return decorator

def get_stats_data():
    """获取统计数据"""
    avg_time = stats['total_processing_time'] / stats['total_requests'] if stats['total_requests'] > 0 else 0
    return {
        'total_requests': stats['total_requests'],
        'successful_requests': stats['successful_requests'],
        'failed_requests': stats['failed_requests'],
        'success_rate': f"{(stats['successful_requests'] / stats['total_requests'] * 100):.2f}%" if stats['total_requests'] > 0 else "0%",
        'average_processing_time': f"{avg_time:.3f}s",
        'endpoints': stats['endpoints']
    }
