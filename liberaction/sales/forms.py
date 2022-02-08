from django import forms
from .models import Cart, CartItem
from liberaction.core.models import BaseProduct

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemForm(forms.ModelForm):
    cart = forms.ModelChoiceField(
        queryset=Cart.objects.all(),
        widget=forms.HiddenInput()
    )
    product = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        disabled=True
    )
    class Meta:
        model = CartItem
        fields = '__all__'
