from django import forms
from .models import BaseProduct, Product, Service, Tag
from django.contrib.auth.models import User

class BaseProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(), disabled=True,
        widget=forms.HiddenInput()
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
    class Meta:
        model = BaseProduct
        fields = '__all__'

class ProductForm(forms.ModelForm):
    base = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        required=False, disabled=True,
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Product
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    base = forms.ModelChoiceField(
        queryset=BaseProduct.objects.all(),
        required=False, disabled=True,
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Service
        fields = '__all__'
