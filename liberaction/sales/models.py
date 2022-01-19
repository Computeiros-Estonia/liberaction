from django.db import models
from django.contrib.auth.models import User
from liberaction.core.models import BaseProduct

class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='comprador')
    freight = models.FloatField('frete')

    class Meta:
        verbose_name = 'carrinho de compras'
        verbose_name_plural = 'carrinhos de compras'

    def __str__(self):
        return f'#{self.id} {self.buyer}'

    def get_items(self):
        return CartItem.objects.filter(cart=self)

    def get_subtotal(self):
        subtotal = 0
        for i in self.get_items():
            subtotal += i.product.price

        return subtotal

    def get_total(self):
        return self.get_subtotal() + self.freight

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='carrinho de compras')
    product = models.ForeignKey(BaseProduct, on_delete=models.SET_NULL, null=True, verbose_name='produto')
    product_count = models.IntegerField('unidades')

    class Meta:
        verbose_name = 'item do carrinho'
        verbose_name_plural = 'itens dos carrinhos'

    def __str__(self):
        return f'Cart #{self.cart.id} - {self.product}'
