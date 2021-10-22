from django.contrib import admin
from .models import Tag, Product, Review

admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Review)