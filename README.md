# 小型库存预定模块

## 项目简单说明

这是一个基于 Django 框架开发的库存预定系统，实现了商品查询、库存预定、缓存管理等核心功能。采用分层架构组织，结构清晰。

## 功能实现说明

### 1. 商品查询功能（20 分）

- 通过`search_products`接口实现商品名称搜索
- 使用 Django 的 Q 对象实现模糊查询
- 实现了分页功能，提高性能
- 使用了数据库索引优化查询性能

### 2. 并发预定功能（20 分）

- 使用`select_for_update()`实现悲观锁，防止超卖
- 在事务中进行库存更新操作
- 使用版本号（version）字段实现乐观锁作为备选方案

### 3. 缓存机制（20 分）

- 使用 Redis 作为缓存存储
- 实现了缓存查询和更新的完整流程
- 在库存更新时同步更新缓存
- 设置合理的缓存过期时间（1 小时）

### 4. 异常处理（20 分）

- 完整的异常处理机制
- 处理了库存不足、数据库异常等情况
- 统一的错误返回格式
- 异常日志记录

### 5. 面向对象设计（20 分）

- 清晰的三层架构：
  - 模型层（Models）：`Product`和`StockRecord`
  - 服务层（Services）：`StockService`
  - 视图层（Views）：处理 HTTP 请求
- 代码复用和职责分离
- 遵循单一职责原则

## 使用说明

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Redis

在 settings.py 中添加以下配置：

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### 3. API 接口说明

#### 搜索商品

- 请求方式：GET
- 接口路径：`/stock/search/`
- 参数：
  - name: 商品名称（可选）
  - page: 页码（默认 1）
  - page_size: 每页数量（默认 10）

#### 查询库存

- 请求方式：GET
- 接口路径：`/stock/{product_id}/`
- 参数：
  - product_id: 商品 ID（路径参数）

#### 预定商品

- 请求方式：POST
- 接口路径：`/stock/reserve/`
- 请求体：
  ```json
  {
    "product_id": 1,
    "quantity": 10
  }
  ```

## 技术特点

1. 使用 Django ORM 进行数据库操作
2. 采用 Redis 实现缓存机制
3. 使用悲观锁和乐观锁保证并发安全
4. 实现了完整的分层架构
5. 统一的异常处理和响应格式
