from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('basket_summary/', views.basket_summary, name='basket_summary'),
]
