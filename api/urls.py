# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'images', views.ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('your-data/', views.your_view, name='your_data_view'),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]