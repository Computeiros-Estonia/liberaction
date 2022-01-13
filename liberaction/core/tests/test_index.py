import pytest
from pytest_django.asserts import assertContains, assertNotContains
from django.urls import reverse
from liberaction.core.models import Product, Review
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create(username='root', password='toor')

@pytest.fixture
def produtos(user):
    return [
        Product.objects.create(name='Web Development',owner=user,description='Awesome websites'),
        Product.objects.create(name='Copywriting',owner=user,description='Awesome copywriting'),
        Product.objects.create(name='Edição de vídeos',owner=user,description='Awesome videos'),
    ]

@pytest.fixture
def resposta_index(client, user, produtos):
    return client.get(reverse('core:index'))

def test_index_page_status_code(resposta_index):
    assert resposta_index.status_code == 200

def test_produtos_presente(resposta_index, produtos):
    for p in produtos:
        assertContains(resposta_index, p)
