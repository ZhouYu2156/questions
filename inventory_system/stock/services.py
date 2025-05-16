from django.core.cache import cache
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, StockRecord

class StockService:
    @staticmethod
    def search_products(name, page=1, page_size=10):
        """
        搜索商品
        使用模糊匹配查询商品，并返回分页结果
        """
        try:
            # 使用Q对象进行模糊查询
            products = Product.objects.filter(
                Q(name__icontains=name)
            ).select_related('stock')

            # 分页处理
            paginator = Paginator(products, page_size)
            current_page = paginator.page(page)

            results = []
            for product in current_page.object_list:
                stock_quantity = StockRecord.get_stock_quantity(product.id)
                results.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'stock_quantity': stock_quantity
                })

            return {
                'total': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page,
                'results': results
            }

        except Exception as e:
            # 记录错误日志
            print(f"Error in search_products: {str(e)}")
            raise

    @staticmethod
    def reserve_product(product_id, quantity):
        """
        预定商品
        使用悲观锁确保并发安全
        """
        try:
            success = StockRecord.reserve_stock(product_id, quantity)
            return success
        except StockRecord.DoesNotExist:
            return False
        except Exception as e:
            # 记录错误日志
            print(f"Error in reserve_product: {str(e)}")
            raise

    @staticmethod
    def get_product_stock(product_id):
        """
        获取商品库存
        优先从缓存获取，缓存未命中则查询数据库
        """
        try:
            return StockRecord.get_stock_quantity(product_id)
        except Exception as e:
            # 记录错误日志
            print(f"Error in get_product_stock: {str(e)}")
            raise 