from django.urls import path
from core.api.v1.products.views import MenuAPIView, ProductListAPIView, ProductByCategoryAPIView, ProductDetailAPIView

urlpatterns = [
    path('menu/', MenuAPIView.as_view(), name='menu-api'),
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('category/<str:category_name>/', ProductByCategoryAPIView.as_view(), name='product-by-category'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
