from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('redirection/', views.service_vs_product_redirection, name='sp_redirection'),
    # Products
    path('create_product/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_details, name='product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    # Service
    path('create_service/', views.create_service, name='create_service'),
    path('service/<int:pk>/', views.service_details, name='service'),
    path('edit_service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:pk>/', views.delete_service, name='delete_service'),
    # Favorites
    path('favorites/', views.favorites, name='favorites'),
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:pk>/', views.remove_from_favorites, name='remove_from_favorites'),
]
