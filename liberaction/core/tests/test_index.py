import pytest
from pytest_django.asserts import assertContains, assertNotContains
from django.urls import reverse
from liberaction.core.models import BaseProduct, Product, Review
from liberaction.users.models import User

@pytest.fixture
def user(db):
    return User.objects.create(email='root@liberaction.com.br', password='toor')

@pytest.fixture
def produtos(user):
    base_products = [
        BaseProduct.objects.create(name='Camiseta',owner=user, description='Awesome t-shirts', price=100),
        BaseProduct.objects.create(name='Computador Gamer',owner=user, description='Awesome speed', price=100),
        BaseProduct.objects.create(name='Suplementos',owner=user, description='Awesome stuff', price=100),
    ]
    products = []
    for p in base_products:
        product = Product.objects.create(base=p)
        products.append(product)
    return products

@pytest.fixture
def resposta_index(client, user, produtos):
    return client.get(reverse('core:index'))

def test_index_page_status_code(resposta_index):
    assert resposta_index.status_code == 200

def test_produtos_presente(resposta_index, produtos):
    for p in produtos:
        assertContains(resposta_index, p)
