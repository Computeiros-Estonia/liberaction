from django.contrib import admin
from .models import Tag, BaseProduct, Product, Review, Album, Picture

admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(BaseProduct)
admin.site.register(Review)
admin.site.register(Album)
admin.site.register(Picture)