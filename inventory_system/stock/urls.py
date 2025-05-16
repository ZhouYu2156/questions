from django.urls import path
from . import views

urlpatterns = [
    path('/stock/search/', views.search_products, name='search_products'),
    path('stock/<int:product_id>/', views.get_stock, name='get_stock'),
    path('/stock/reserve/', views.reserve_stock, name='reserve_stock'),
] 