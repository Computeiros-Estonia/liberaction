from django import forms

from .models import Basket, BasketItem
from liberaction.core.models import BaseProduct


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = '__all__'

class BasketItemForm(forms.ModelForm):
    basket = forms.ModelChoiceField(
        queryset=Basket.objects.all(),
        widget=forms.HiddenInput()
    )
    product = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        disabled=True
    )
    class Meta:
        model = BasketItem
        fields = '__all__'
