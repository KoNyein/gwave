from django.contrib import admin
from .models import Category, Product, Sale, SaleItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['emoji', 'name']


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['product_name', 'price_mmk', 'quantity', 'subtotal']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['emoji', 'name', 'category', 'price_mmk', 'stock', 'is_low_stock', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    list_editable = ['stock', 'is_active']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'total', 'currency', 'payment_method', 'cashier', 'created_at']
    list_filter = ['currency', 'payment_method', 'created_at']
    inlines = [SaleItemInline]
    readonly_fields = ['sale_number', 'created_at']
