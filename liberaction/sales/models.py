from django.db import models
from django.utils import timezone

from liberaction.users.models import User
from liberaction.core.models import BaseProduct

class Basket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='cliente')
    is_active = models.BooleanField(default=True, verbose_name='ativa', help_text='Determina se a cesta de compras está ativa.')
    class Meta:
        verbose_name = 'cesta de compras'
        verbose_name_plural = 'cestas de compras'

    def __str__(self):
        return f'Basket #{self.id}'

    def get_items(self):
        return BasketItem.objects.filter(basket=self)
    
    def get_price(self):
        return sum(i.get_price() for i in self.get_items())

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='cesta de compras')
    product = models.ForeignKey(BaseProduct, on_delete=models.SET_NULL, null=True, verbose_name='produto')
    product_count = models.IntegerField('unidades')

    class Meta:
        verbose_name = 'item da cesta'
        verbose_name_plural = 'itens da cesta'

    def __str__(self):
        return f'Basket #{self.basket.id} - {self.product}'

    def get_price(self):
        return self.product.price * self.product_count

class Sale(models.Model):
    basket = models.OneToOneField(Basket, on_delete=models.SET_NULL, null=True, verbose_name='cesta de compras')
    freight = models.FloatField('frete')
    date = models.DateField("data", default=timezone.now, null=True, blank=True)
    note = models.TextField('observação', blank=True, null=True)
    INSTALLMENT_CHOICES = ((1, '1x'),(2, '2x'),(3, '3x'),
                           (4, '4x'),(5, '5x'),(6, '6x'),
                           (7, '7x'),(8, '8x'),(9, '9x'),
                           (10, '10x'),(11, '11x'),(12, '12x'))
    installments = models.IntegerField("parcelas", choices=INSTALLMENT_CHOICES, default=1)

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __str__(self):
        return f'Sale #{self.id}'

    def get_customer(self):
        return self.basket.customer

    def get_items(self):
        return self.basket.get_items()

    def get_subtotal(self):
        return self.basket.get_price()

    def get_total(self):
        return self.get_subtotal() + self.freight

    def get_installment(self):
        return self.get_total() / self.installment
