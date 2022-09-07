import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from liberaction.core.models import BaseProduct
from liberaction.users.models import User
from liberaction.sales.models import Basket, BasketItem


# Fixtures

@pytest.fixture
def user(db):
    return User.objects.create_user(email='user@email.com', password='123')

@pytest.fixture
def base_product(user):
    return BaseProduct.objects.create(
        name='Produto1',
        owner=user,
        description='Description',
        price=100
    )

@pytest.fixture
def customer(db):
    return User.objects.create_user(email='customer@email.com', password='12345')

@pytest.fixture
def basket(base_product, customer):
    return Basket.objects.create(customer=customer)


# POST tests

@pytest.fixture
def basket_add_response(client, customer, basket, base_product):
    client.force_login(customer)
    return client.post(reverse('sales:basket_add'), data={'base_product': base_product.id, 'product_count': 1})

def test_post_basket_add_redirection(basket_add_response, base_product):
    assertRedirects(basket_add_response, reverse('core:product', kwargs={'pk': base_product.id}))

def test_bskt_updated(basket_add_response, basket):
    assert len(basket.get_items()) > 0


@pytest.fixture
def basket_remove_response(client, customer, basket, base_product):
    bitem = BasketItem.objects.create(basket=basket, product=base_product, product_count=1)
    client.force_login(customer)
    return client.post(reverse('sales:basket_remove', kwargs={'pk': bitem.id}))

def test_bskt_remove_redirection(basket_remove_response):
    assertRedirects(basket_remove_response, reverse('sales:basket_summary'))

def test_bskt_item_deleted(basket_remove_response, basket):
    assert not BasketItem.objects.exists()
    assert len(basket.get_items()) == 0
