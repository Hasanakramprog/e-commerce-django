from django.contrib import admin
from .models import Product
from image.models import Image

class ImageInline(admin.TabularInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(Image)
admin.site.register(Product, ProductAdmin)
