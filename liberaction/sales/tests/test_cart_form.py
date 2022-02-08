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
    return client.get(reverse('sales:cart', kwargs={'pk': cart.pk}))

def test_get_response_status_code(cart_response):
    assert cart_response.status_code == 200

# def test_formset_present(cart_response):
#     assertContains(cart_response, '<input type="hidden" name="form-TOTAL_FORMS"')

def test_item_present(cart_response):
    assertContains(cart_response, '<input type="number" name="form-0-product_count" value="1"')