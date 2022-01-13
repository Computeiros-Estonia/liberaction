from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Product
        fields = '__all__'
