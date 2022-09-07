from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import BasketItemForm
from .models import Basket, BasketItem

@login_required(login_url='/users/login/')
def basket_summary(request):
    basket_filter = Basket.objects.filter(customer=request.user, is_active=True)
    basket = basket_filter[0] if basket_filter else Basket.objects.create(customer=request.user)
