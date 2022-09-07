from django.urls import reverse
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BasketItemForm
from .models import Basket, BasketItem

@login_required(login_url='/users/login/')
def basket_summary(request):
    basket_filter = Basket.objects.filter(customer=request.user, is_active=True)
    basket = basket_filter[0] if basket_filter else Basket.objects.create(customer=request.user)
    BasketItemFormSet = modelformset_factory(BasketItem, form=BasketItemForm, extra=0)
    if request.method == 'POST':
        formset = BasketItemFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            if 'create_sale' in request.POST:
                # TODO: create sale view
                pass
            return redirect(request.path)
    else:
        formset = BasketItemFormSet(queryset=basket.get_items())
    
    context = {
        'title': 'Cesta de Compras',
        'basket': basket,
        'item_formset': formset,
    }
    return render(request, 'sales/basket_summary.html', context)
