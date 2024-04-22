# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet,basename='category')
router.register(r'products', views.ProductViewSet)
router.register(r'images', views.ImageViewSet)
# router.register(r'category-delete', views.CategoryDeleteView)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('all-products/', views.all_products, name='your_product_view'),
    path('all-categories/', views.all_categories, name='your_category_view'),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]