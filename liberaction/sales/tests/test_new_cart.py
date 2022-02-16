import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from liberaction.core.models import BaseProduct
from liberaction.users.models import User
from liberaction.sales.models import Cart, CartItem

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
def cart(base_product):
    cart = Cart.objects.create()
    item = CartItem.objects.create(cart=cart, product=base_product, product_count=1)
    return cart

@pytest.fixture
def cart_response(client, user, cart):
    client.force_login(user)
    return client.post(reverse('sales:cart', kwargs={'pk': cart.pk}))
