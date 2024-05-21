# views.py
from rest_framework import viewsets,permissions
from api.serializers import CategorySerializer
from category.models import Category
from api.serializers import ProductSerializer
from api.serializers import ImageSerializer
from product.models import Product
from image.models import Image
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from whatsapp_api_client_python import API
from django.db.models import OrderBy

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # Replace with your queryset logic
    serializer_class = CategorySerializer    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
# class ImageViewSet(viewsets.ModelViewSet):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     # Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()  # Consider permission filtering if needed
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Example permission

    # Add access control logic here (e.g., IsAdminUser permission class or custom permissions)    
class CategoryProductsView(APIView):
    def get(self, request, category_name):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()  # All products in the database
    serializer_class = ProductSerializer

def slice_list(data, limit, skip=0):

    return data[skip:skip + limit] if len(data) >= skip + limit else data[skip:]

def all_products(request,limit,skip):
    # Retrieve data from the table

    

    products =Product.objects.all().order_by('-id')   # Retrieve all products
    products=slice_list(products,limit,skip)    

    images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images

    # p_list=[]
    p_list={'products':[]}
    for product in products:
        product = Product.objects.select_related('category').get(pk=product.id)
        category_name = product.category.name  # Access category name
        product = Product.objects.select_related('brand').get(pk=product.id)
        brand_name = product.brand.name  # Access category name
        
        imagess=[]
       
        for image in images.filter(product=product): 
            imagess.append(image.get_image_url() )  # Access image URL
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

def product_detail_view(request, pk):
  
  p_list={'products':[]}
  try:
    # Get the product with the specified ID
    product = Product.objects.get(pk=pk)
  except Product.DoesNotExist:
     response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
     return response
  products = Product.objects.all()  # Retrieve all products

  images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images
  product = Product.objects.select_related('category').get(pk=product.id)
  category_name = product.category.name  # Access category name
  product = Product.objects.select_related('brand').get(pk=product.id)
  brand_name = product.brand.name  # Access category name

  imagess=[]
  for image in images.filter(product=product):  # Find images for this product
        imagess.append(settings.API_DOMAIN+'/'+image.image.url)  # Access image URL
  p_list={'id':product.id,'title':product.title,'description':product.description,
                    'price':int(product.price),'discountPercentage':float(product.discount_percentage),'rating':float(product.rating),'stock':product.stock,'brand':brand_name,'thumbnail':product.get_thumbnail_url(),'category':category_name,'images':imagess} 
  response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
  return response
def product_by_category(request,keyword):
    p_list={'products':[]}

    try:            category = Category.objects.get(name=keyword)
    except Category.DoesNotExist:
            response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
            return response
    products = Product.objects.all()  # Retrieve all products

    images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images
    products = Product.objects.filter(category=category)
    for product in products:
        product = Product.objects.select_related('category').get(pk=product.id)
        category_name = product.category.name  # Access category name
        product = Product.objects.select_related('brand').get(pk=product.id)
        brand_name = product.brand.name  # Access category name
        
        imagess=[]
        for image in images.filter(product=product):  # Find images for this product
            imagess.append(image.image.url)  # Access image URL
        p_list.get('products').append({'id':product.id,'title':product.title,'description':product.description,
                       'price':int(product.price),'discountPercentage':float(product.discount_percentage),'rating':float(product.rating),'stock':product.stock,'brand':brand_name,'thumbnail':product.get_thumbnail_url(),'category':category_name,'images':imagess}) 


    response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
    return response


def product_search_view(request):
  query = request.GET.get('q', '')  # Get the search query from 'q' parameter
  if query:
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
  else:
    products = Product.objects.all()  # Return all products if no query is provided
  images = Image.objects.filter(product__in=products).select_related('product')  # Prefetch images

    # p_list=[]
  p_list={'products':[]}
  for product in products:
        product = Product.objects.select_related('category').get(pk=product.id)
        category_name = product.category.name  # Access category name
        product = Product.objects.select_related('brand').get(pk=product.id)
        brand_name = product.brand.name  # Access category name
        
        imagess=[]
        for image in images.filter(product=product):  # Find images for this product
            imagess.append(image.image.url)  # Access image URL
        p_list.get('products').append({'id':product.id,'title':product.title,'description':product.description,
                       'price':int(product.price),'discountPercentage':float(product.discount_percentage),'rating':float(product.rating),'stock':product.stock,'brand':brand_name,'thumbnail':product.get_thumbnail_url(),'category':category_name,'images':imagess}) 

  response = JsonResponse(p_list, safe=False)  # Set safe=False for non-primitive data types
  return response

    

class MessageView(APIView):
        def post(self, request):
            data = request.data
            checkout_msg='**Checkout Summary:**'
            for d in data :
                name=d.get('name')
                number=d.get('number')
                location=d.get('location')
                a=self.format_checkout_message(d.get('title'),d.get('quantity'),d.get('price'))
                checkout_msg+=a
            checkout_msg+='Customer Number: {} /n Customer Name: {} /n Customer Location: {}'.format(name,number,location)
            greenAPI = API.GreenAPI(
        "7103938518", "e33b3980940f40b5abd614cc34a6d867faf9136729524901ae")
            response = greenAPI.sending.sendMessage("96170639378@c.us", checkout_msg)

            print(response.data) 
           
            return Response([1,2,3], status=201)  # Created (201) status
        
        def format_checkout_message(self,product_title,product_id,product_price):  

 

            return f"""
            ***********************************************

            * Product ID: {product_id}
            * Product Title: {product_title}
            * Price: ${product_price}

            ***********************************************
            """

            

            # # Get the formatted checkout message
            # checkout_message = format_checkout_message(product)

            # # Print the checkout message
            # print(checkout_message)

