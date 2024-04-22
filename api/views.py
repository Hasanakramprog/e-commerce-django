# views.py
from rest_framework import viewsets,generics

from api.serializers import CategorySerializer
from category.models import Category
from api.serializers import ProductSerializer
from api.serializers import ImageSerializer
from product.models import Product
from image.models import Image
from django.http import JsonResponse,HttpResponse
import json
from rest_framework.generics import RetrieveAPIView,RetrieveDestroyAPIView
from .serializers import ProductSerializer
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # Replace with your queryset logic
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

def all_products(request):
    # Retrieve data from the table
    

    products = Product.objects.all()  # Retrieve all products
    images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images

    # p_list=[]
    p_list={'products':[]}
    for product in products:
        product = Product.objects.select_related('category').get(pk=product.id)
        category_name = product.category.name  # Access category name
        product = Product.objects.select_related('brand').get(pk=product.id)
        brand_name = product.brand.name  # Access category name
        print("Images:")
        imagess=[]
        for image in images.filter(product=product):  # Find images for this product
            imagess.append(image.image.url)  # Access image URL
        p_list.get('products').append({'id':product.id,'title':product.title,'description':product.description,
                       'price':int(product.price),'discountPercentage':float(product.discount_percentage),'rating':float(product.rating),'stock':product.stock,'brand':brand_name,'thumbnail':product.get_thumbnail_url(),'category':category_name,'images':imagess})    
    response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
    return response

def all_categories(request):
    # Retrieve data from the table
    

    categories = Category.objects.all()  # Retrieve all products

    # p_list=[]
    p_list=[]
    for category in categories:
      p_list.append(category.name)    
    response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
    return response


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
