from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'created_at', 'available']
    list_filter = ['available', 'created_at', 'updated_at']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}