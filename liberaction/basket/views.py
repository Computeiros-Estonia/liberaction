from django.shortcuts import render

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/basket_summary.html', {'basket': basket})
