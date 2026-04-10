from django.urls import path
from .views import catalog_list, product_detail

urlpatterns = [
    path('', catalog_list, name='catalog_list'),
    path('<int:pk>/', product_detail, name='product_detail'),
]