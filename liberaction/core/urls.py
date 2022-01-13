from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_product/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_details, name='product'),
]
