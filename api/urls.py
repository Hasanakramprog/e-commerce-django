# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from .views import MessageView
router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet,basename='category')
# router.register(r'products', views.ProductViewSet)
router.register(r'images', views.ImageViewSet)
# router.register(r'category-delete', views.CategoryDeleteView)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('all-products/<int:limit>/<int:skip>/', views.all_products, name='your_product_view'),
    path('all-categories/', views.all_categories, name='your_category_view'),
    path('products/category/<str:keyword>/', views.product_by_category, name='produc_by_category'),
    path('products/<int:pk>/', views.product_detail_view, name='product_by_id'),
    path('products/serach/', views.product_search_view, name='serach'),
    # path('products/order/', views.product_order_view, name='order'),
    path('products/order/', MessageView.as_view(), name='order'),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)