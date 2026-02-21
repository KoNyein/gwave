from django.urls import path
from . import views

urlpatterns = [
    # Main POS
    path('', views.pos_view, name='pos'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Products CRUD
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),

    # Sales History
    path('sales/', views.sales_history_view, name='sales_history'),
    path('sales/<int:pk>/', views.sale_detail_view, name='sale_detail'),

    # API endpoints (JSON)
    path('api/products/', views.api_products, name='api_products'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/sales-chart/', views.api_sales_chart, name='api_sales_chart'),
]
