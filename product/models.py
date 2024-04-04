from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from category.models import Category  # Import the Category model
from brand.models import Brand 

class Product(models.Model):
    id = models.IntegerField(primary_key=True)  # Assuming the ID is unique
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # Foreign key to Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category model
    # thumbnail = models.URLField()
    # images = models.JSONField(blank=True,null=True)
    images = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')

    def __str__(self):
        return self.title
