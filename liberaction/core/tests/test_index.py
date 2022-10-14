import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from liberaction.core.models import BaseProduct, Product


# @pytest.fixture
# def user(db):
#     return User.objects.create(email='root@liberaction.com.br', password='toor')

@pytest.fixture
def produtos(user):
    return [
        Product.objects.create(name='Camiseta',owner=user, description='Awesome t-shirts', price=100),
        Product.objects.create(name='Computador Gamer',owner=user, description='Awesome speed', price=100),
        Product.objects.create(name='Suplementos',owner=user, description='Awesome stuff', price=100),
    ]

@pytest.fixture
def resposta_index(client, user, produtos):
    return client.get(reverse('core:index'))

def test_index_page_status_code(resposta_index):
    assert resposta_index.status_code == 200

def test_produtos_presente(resposta_index, produtos):
    for p in produtos:
        assertContains(resposta_index, p)
