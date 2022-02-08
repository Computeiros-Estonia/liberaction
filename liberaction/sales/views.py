from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import CartItemForm
from .models import Cart, CartItem

@login_required(login_url='/users/login/')
def cart(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Http404()
        
    CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, extra=0)
    if request.method == 'POST':
        pass
    else:
        formset = CartItemFormSet(queryset=CartItem.objects.filter(cart=cart))
    
    context = {
        'title': 'Carrinho de Compras',
        'formset': formset,
    }
    return render(request, 'sales/cart.html', context)
