from django.contrib import admin
from django.http import HttpRequest

from parler.admin import TranslatableAdmin

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request:HttpRequest, obj=None) -> dict:
        return {
            'slug': ('name',),
        }

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated',
    ]
    list_filter = ['available', 'created', 'updated',
    ]
    list_editable = ['price', 'available',
    ]
    
    def get_prepopulated_fields(self, request:HttpRequest, obj=None) -> dict:
        return {
            'slug': ('name',),
        }
