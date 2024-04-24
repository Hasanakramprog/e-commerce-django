from django.db import models
from product.models import Product

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to your main model
    image = models.ImageField(upload_to='thumbnail')  # Path to store images
    caption = models.CharField(max_length=255, blank=True)  # Optional caption field

