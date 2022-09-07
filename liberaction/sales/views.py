from django.urls import reverse
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import BasketItemForm
from .models import Basket, BasketItem
from liberaction.core.models import BaseProduct

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


@login_required(login_url='/users/login/')
def basket_add(request):
    if request.method == 'POST':
        # Clean form data
        form = BasketItemForm(request.POST)
        if form.is_valid():
            base_product = form.cleaned_data.get('base_product')
            product_count = form.cleaned_data.get('product_count')
            # Get and update basket
            basket_filter = Basket.objects.filter(customer=request.user, is_active=True)
            basket = basket_filter[0] if basket_filter else Basket.objects.create(customer=request.user)
            BasketItem.objects.create(basket=basket, product=base_product, product_count=product_count)
            messages.success(request, 'Cesta atualizada com sucesso.')
            return redirect(reverse('core:product', kwargs={'pk': base_product.pk}))


@login_required(login_url='/users/login/')
def basket_remove(request, pk):
    item = get_object_or_404(BasketItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Cesta atualizada com sucesso.')
    return redirect(reverse('sales:basket_summary'))
