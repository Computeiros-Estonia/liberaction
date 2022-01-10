from django.shortcuts import render
from .models import Product

def index(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'core/index.html', context)

def product(request, pk):
    context = {
        'product': Product.objects.get(id=pk),      
    }
    return render(request, 'core/product.html', context) 

def register(request):
    return render(request, 'core/register.html')

def login(request):
    return render(request, 'core/login.html')
