# views.py
from rest_framework import viewsets

from api.serializers import CategorySerializer
from category.models import Category
from api.serializers import ProductSerializer
from api.serializers import ImageSerializer
from product.models import Product
from image.models import Image
from django.http import JsonResponse


from rest_framework.generics import RetrieveAPIView
from .serializers import ProductSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # Create your views here.


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()  # All products in the database
    serializer_class = ProductSerializer


from django.shortcuts import render

def your_view(request):
    # Retrieve data from the table


    products = Product.objects.all()  # Retrieve all products
    images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images

    p_list=[]
    for product in products:
        
        print("Images:")
        imagess=[]
        for image in images.filter(product=product):  # Find images for this product
            imagess.append(image.image.url)  # Access image URL
        p_list.append({'id':product.id,'images':imagess})    
        print(p_list)  
    response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
    return response
