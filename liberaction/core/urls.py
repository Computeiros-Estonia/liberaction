from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product, name='product'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
