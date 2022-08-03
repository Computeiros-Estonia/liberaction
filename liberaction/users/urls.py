from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # CRUD Addresses
    path('create_address/', views.create_address, name='create_address'),
    path('user_addresses/<int:user_pk>', views.user_addresses, name='user_addresses'),
    path('update_address/<int:pk>', views.update_address, name='update_address'),
    path('delete_address/<int:pk>', views.delete_address, name='delete_address'),
]
