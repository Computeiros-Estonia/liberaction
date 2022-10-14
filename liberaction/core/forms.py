from django import forms
from .models import BaseProduct, Product, Service, Tag
from liberaction.users.models import User


class ProductForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput()
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
    class Meta:
        model = Product
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput()
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
    class Meta:
        model = Service
        fields = '__all__'
