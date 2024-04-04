from django.contrib import admin
from .models import Brand  # Assuming your model is named Product
class BrandAdmin(admin.ModelAdmin):
    list_display = (['id','name'])  # Include other relevant fields
admin.site.register(Brand,BrandAdmin)  # Register the Product model
