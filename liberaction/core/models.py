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

    def __str__(self):
        return self.name

    def get_albums(self):
        return Album.objects.filter(product=self)

    def get_pictures(self):
        albums = self.get_albums()
        if albums:
            return Picture.objects.filter(album=albums.first())
        else:
            return None

class Album(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='produto')

    def __str__(self):
        return f'{self.product}'
    
    def get_pictures(self):
        pictures = Picture.objects.filter(album=self)
        if pictures:
            return pictures.order_by('index')

class Picture(models.Model):
    img = models.ImageField(verbose_name='imagem')
    index = models.IntegerField(verbose_name='índice')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.index} {self.img.name}'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='produto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    SCORE_CHOICES = ((1, 1),
        (2, 2), (3, 3), 
        (4, 4), (5, 5),
    )
    score = models.IntegerField(verbose_name='nota', choices=SCORE_CHOICES)
    comment = models.TextField(verbose_name='comentário')
