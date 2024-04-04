from django.contrib import admin
from .models import Category  # Assuming your model is named Product
class CategoryAdmin(admin.ModelAdmin):
    list_display = (['id','name'])  # Include other relevant fields
admin.site.register(Category,CategoryAdmin)  # Register the Product model
