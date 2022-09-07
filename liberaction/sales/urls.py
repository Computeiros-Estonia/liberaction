from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Basket
    path('basket_summary/', views.basket_summary, name='basket_summary'),
    path('basket_add/', views.basket_add, name='basket_add'),
    path('basket_remove/<int:pk>/', views.basket_remove, name='basket_remove'),
]
