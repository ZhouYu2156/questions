from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .services import StockService

# Create your views here.

@require_http_methods(["GET"])
def search_products(request):
    """搜索商品接口"""
    try:
        name = request.GET.get('name', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        result = StockService.search_products(name, page, page_size)
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e),
            'data': None
        })

@require_http_methods(["GET"])
def get_stock(request, product_id):
    """获取商品库存接口"""
    try:
        quantity = StockService.get_product_stock(product_id)
        return JsonResponse({
            'code': 200,
            'message': 'success',
            'data': {'quantity': quantity}
        })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e),
            'data': None
        })

@csrf_exempt
@require_http_methods(["POST"])
def reserve_stock(request):
    """预定商品接口"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not all([product_id, quantity]):
            return JsonResponse({
                'code': 400,
                'message': '参数错误',
                'data': None
            })

        success = StockService.reserve_product(product_id, quantity)
        
        if success:
            return JsonResponse({
                'code': 200,
                'message': '预定成功',
                'data': None
            })
        else:
            return JsonResponse({
                'code': 400,
                'message': '库存不足',
                'data': None
            })
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': str(e),
            'data': None
        })
