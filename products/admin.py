from django.contrib import admin
from .models import Product, Category, Review, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
   
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ProductImage)