from faulthandler import disable
from django import forms
from .models import Product
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(), disabled=True)
    class Meta:
        model = Product
        fields = '__all__'
