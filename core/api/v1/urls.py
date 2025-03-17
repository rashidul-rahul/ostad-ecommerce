from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include('core.api.v1.users.urls')),
    path('products/', include('core.api.v1.products.urls')),
]
