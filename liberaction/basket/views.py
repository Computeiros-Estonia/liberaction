from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .basket import Basket
from liberaction.core.models import BaseProduct, Product


def basket_summary(request):
    basket = Basket(request)
    products = Product.objects.filter(pk__in=basket.basket.values())
    context = {
        'basket': list(zip(basket.basket, products)),
    }
    return render(request, 'basket/basket_summary.html', context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(BaseProduct, pk=product_id)
        basket_qty = basket.__len__()
        basket.add(product=product, qty=product_qty)
        return JsonResponse({'qty': basket_qty})
