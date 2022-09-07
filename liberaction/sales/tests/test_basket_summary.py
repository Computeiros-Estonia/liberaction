import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from liberaction.core.models import BaseProduct
from liberaction.users.models import User
from liberaction.sales.models import Basket, BasketItem

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
    basket = Basket.objects.create(customer=customer)
    BasketItem.objects.create(basket=basket, product=base_product, product_count=1)
    return basket

# GET
@pytest.fixture
def basket_response(client, customer, basket):
    client.force_login(customer)
    return client.get(reverse('sales:basket_summary'))

def test_get_bskt_smry_status_code(basket_response):
    assert basket_response.status_code == 200

def test_form_present(basket_response):
    assertContains(basket_response, f'<form action="{reverse("sales:basket_summary")}"')
    assertContains(basket_response, '<input type="hidden" name="form-TOTAL_FORMS" value="1"')

def test_item_present(basket_response, base_product):
    assertContains(basket_response, f'<input type="hidden" name="form-0-product" value="{base_product.id}"')

# POST
@pytest.fixture
def post_basket_smry_response(client, customer, basket):
    client.force_login(customer)
    return client.post(reverse('sales:basket_summary'), data={
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '1',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-id': basket.get_items().first().id,
        'form-0-basket': basket.id,
        'form-0-product_count': '2',
    })

# For debug purposes only, DO NOT UNCOMMENT.
# def test_form_errors(post_basket_smry_response):
#     assert not post_basket_smry_response.context['formset'].errors

def test_post_bskt_smry_redirection(post_basket_smry_response):
    assertRedirects(post_basket_smry_response, reverse('sales:basket_summary'))

def test_bskt_item_updated(post_basket_smry_response, basket):
    assert basket.get_items()[0].product_count == 2
