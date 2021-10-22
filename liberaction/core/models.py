from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='fornecedor')
    description = models.TextField(verbose_name='descrição')

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='produto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    SCORE_CHOICES = ((1, 1),
        (2, 2), (3, 3), 
        (4, 4), (5, 5),
    )
    score = models.IntegerField(verbose_name='nota', choices=SCORE_CHOICES)
    comment = models.TextField(verbose_name='comentário')
