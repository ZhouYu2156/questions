# 导入必要的模块
from django.db import models        # Django的模型类
from django.core.cache import cache # Django的缓存功能
from django.db import transaction   # 数据库事务支持

class Product(models.Model):
    # 商品模型类
    name = models.CharField(max_length=200, db_index=True)  # 商品名称，建立索引
    description = models.TextField(blank=True)              # 商品描述，可为空
    created_at = models.DateTimeField(auto_now_add=True)   # 创建时间，自动添加
    updated_at = models.DateTimeField(auto_now=True)       # 更新时间，自动更新

    class Meta:
        indexes = [
            models.Index(fields=['name']), # 在name字段上创建索引，优化查询性能
        ]

    def __str__(self):
        return self.name  # 模型的字符串表示

class StockRecord(models.Model):
    # 库存记录模型类
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')  # 与商品一对一关联
    quantity = models.PositiveIntegerField(default=0)  # 库存数量，非负整数
    version = models.PositiveIntegerField(default=0)   # 版本号，用于乐观锁
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)      # 更新时间

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"  # 字符串表示

    @classmethod
    def get_stock_quantity(cls, product_id):
        """获取商品库存数量的类方法"""
        cache_key = f"stock_quantity_{product_id}"  # 构造缓存键
        quantity = cache.get(cache_key)             # 尝试从缓存获取
        
        if quantity is None:  # 缓存未命中
            try:
                stock_record = cls.objects.get(product_id=product_id)  # 从数据库查询
                quantity = stock_record.quantity
                cache.set(cache_key, quantity, 3600)  # 设置缓存，1小时过期
            except cls.DoesNotExist:
                return 0  # 商品不存在返回0
        
        return quantity

    @classmethod
    def reserve_stock(cls, product_id, quantity):
        """预定库存的类方法"""
        with transaction.atomic():  # 开启事务
            stock_record = (cls.objects
                          .select_for_update()  # 使用悲观锁锁定记录
                          .get(product_id=product_id))
            
            if stock_record.quantity >= quantity:  # 检查库存是否充足
                stock_record.quantity -= quantity  # 扣减库存
                stock_record.version += 1         # 更新版本号
                stock_record.save()              # 保存更改
                
                # 更新缓存
                cache_key = f"stock_quantity_{product_id}"
                cache.set(cache_key, stock_record.quantity, 3600)
                
                return True
            return False  # 库存不足