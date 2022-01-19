from django import forms
from .models import BaseProduct, Product, Tag
from django.contrib.auth.models import User

class BaseProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(), disabled=True)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
    class Meta:
        model = BaseProduct
        fields = '__all__'

class ProductForm(forms.ModelForm):
    base = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        required=False, disabled=True)
    class Meta:
        model = Product
        fields = '__all__'
