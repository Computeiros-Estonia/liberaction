from django.db import models
from liberaction.users.models import User
from liberaction.core.models import BaseProduct

class Cart(models.Model):
    is_open = models.BooleanField(default=True, verbose_name='Carrinho em aberto', help_text='Determina se a compra do carrinho está em aberto.')
    class Meta:
        verbose_name = 'carrinho de compras'
        verbose_name_plural = 'carrinhos de compras'

    def __str__(self):
        return f'Carrinho #{self.id}'

    def get_items(self):
        return CartItem.objects.filter(cart=self)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='carrinho de compras')
    product = models.ForeignKey(BaseProduct, on_delete=models.SET_NULL, null=True, verbose_name='produto')
    product_count = models.IntegerField('unidades')

    class Meta:
        verbose_name = 'item do carrinho'
        verbose_name_plural = 'itens dos carrinhos'

    def __str__(self):
        return f'Cart #{self.cart.id} - {self.product}'

class Sale(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name='carrinho de compras')
    freight = models.FloatField('frete')

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __str__(self):
        return f'Sale #{self.id} - {self.buyer}'

    def get_items(self):
        return self.cart.get_items()

    def get_subtotal(self):
        subtotal = 0
        for i in self.get_items():
            subtotal += i.product.price

        return subtotal

    def get_total(self):
        return self.get_subtotal() + self.freight
