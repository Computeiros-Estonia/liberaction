from django.db import models
from liberaction.users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')

    def __str__(self):
        return self.name

class BaseProduct(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='fornecedor')
    description = models.TextField(verbose_name='descrição')
    price = models.FloatField(verbose_name='Preço')

    def __str__(self):
        return f'{self.name} by {self.owner}'

    def get_albums(self):
        return Album.objects.filter(base_product=self)

    def get_first_picture(self):
        albums = self.get_albums()
        if albums:
            return Picture.objects.filter(album=albums.first()).first()
        else:
            return None

    def get_pictures(self):
        albums = self.get_albums()
        if albums:
            return Picture.objects.filter(album=albums.first())
        else:
            return None
    
    def get_reviews(self):
        return Review.objects.filter(product=self)

class Service(models.Model):
    base = models.OneToOneField(BaseProduct, on_delete=models.CASCADE)
    is_negotiable = models.BooleanField(default=False, verbose_name='negociável')

    class Meta:
        verbose_name = 'serviço'

    def __str__(self):
        return self.base.name

    def get_name(self):
        return self.base.name

    def get_owner(self):
        return self.base.owner

    def get_description(self):
        return self.base.description

    def get_price(self):
        return self.base.price

    def get_pictures(self):
        return self.base.get_pictures()


class Product(models.Model):
    base = models.OneToOneField(BaseProduct, on_delete=models.CASCADE)
    is_new = models.BooleanField(default=True, verbose_name='novo')
    quantity = models.IntegerField(default=1, verbose_name= 'quantidade')

    class Meta:
        verbose_name = 'produto'

    def __str__(self):
        return self.base.name
    
    def get_name(self):
        return self.base.name

    def get_owner(self):
        return self.base.owner

    def get_description(self):
        return self.base.description

    def get_price(self):
        return self.base.price

    def get_pictures(self):
        return self.base.get_pictures()

class Album(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, verbose_name='produto')

    def __str__(self):
        return f'{self.base_product}'
    
    def get_pictures(self):
        pictures = Picture.objects.filter(album=self)
        if pictures:
            return pictures.order_by('index')

class Picture(models.Model):
    img = models.ImageField(verbose_name='imagem', upload_to='products')
    index = models.IntegerField(verbose_name='índice')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.album.base_product} #{self.index}'

class Review(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, verbose_name='produto')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='usuário')
    SCORE_CHOICES = (
        (1, 1), (2, 2),
        (3, 3), (4, 4), (5, 5),
    )
    score = models.IntegerField(verbose_name='nota', choices=SCORE_CHOICES)
    comment = models.TextField(verbose_name='comentário')

    def __str__(self):
        return f'{self.base_product} ({self.score})'
