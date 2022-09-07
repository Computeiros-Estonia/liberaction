from email.policy import default
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
        widget=forms.HiddenInput(),
    )
    product = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True,
    )
    product_count = forms.IntegerField(required=True, min_value=1, label='Unidades', initial=1)
    class Meta:
        model = BasketItem
        fields = '__all__'
