from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'address', 'phone_number')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('category_name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    search_fields = ('brand_name',)
    ordering = ('brand_name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color_name',)
    search_fields = ('color_name',)
    ordering = ('color_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'brand', 'color')
    search_fields = ('product_name', 'category__category_name', 'brand__brand_name', 'color__color_name')
    list_filter = ('category', 'brand', 'color')
    ordering = ('product_name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'quantity', 'status', 'address')
    search_fields = ('user__username', 'status')
    list_filter = ('status',)
    ordering = ('-order_date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__product_name')
    list_filter = ('order',)
    ordering = ('order',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'review_date')
    search_fields = ('product__product_name', 'user__username')
    list_filter = ('rating', 'product')
    ordering = ('-review_date',)

