import os
import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from liberaction.settings import BASE_DIR
from liberaction.core.models import Album, Picture, BaseProduct, Product

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create(username='agah', password='testingUser123')

@pytest.fixture
def product(user):
    base = BaseProduct.objects.create(
        name='Bandeira', owner=user,
        description='Bandeira libertária', price=100)
    return Product.objects.create(base=base)

@pytest.fixture
def pictures(product):
    album = Album.objects.create(base_product=product.base)
    return [
        Picture.objects.create(img='test/pic1.jpg', index=0, album=album),
        Picture.objects.create(img='test/pic2.jpg', index=1, album=album),
    ]

# GET
@pytest.fixture
def product_response(client, product, pictures):
    return client.get(
        reverse('core:product',
        kwargs={'pk': product.id})
    )

def test_product_page_status_code(product_response):
    assert product_response.status_code == 200

def test_product_present(product_response, product):
    assertContains(product_response, product)

def test_product_img_present(product_response, product):
    for pic in product.base.get_pictures():
        assertContains(product_response, pic.img.url)
