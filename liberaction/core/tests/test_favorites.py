import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from liberaction.core.models import Product
from liberaction.users.models import User


@pytest.fixture
def product(user):
    return Product.objects.create(
        name='Web dev',
        owner=user,
        description='Coll stuff',
        price=10000
    )


# Vizualizar
@pytest.fixture
def response_favorites(client, product, user):
    user.favorites.add(product)
    client.force_login(user)
    return client.post(reverse('core:favorites'))

def test_favorites_status_code(response_favorites):
    assert response_favorites.status_code == 200

def test_favorite_products_present(response_favorites):
    product = Product.objects.first()
    assertContains(response_favorites, product.name)


# Adicionar
@pytest.fixture
def response_add_to_favorites(client, product, user):
    client.force_login(user)
    return client.post(reverse('core:add_to_favorites', kwargs={'pk': product.pk}))

def test_add_to_favorites_redirection(response_add_to_favorites, product):
    assertRedirects(response_add_to_favorites, reverse('core:product', kwargs={'pk': product.pk}))

def test_product_in_favorites(response_add_to_favorites, product, user):
    assert product.baseproduct_ptr in user.favorites.all()


# Remover
@pytest.fixture
def response_remove_from_favorites(client, product, user):
    user.favorites.add(product)
    client.force_login(user)
    return client.post(reverse('core:remove_from_favorites', kwargs={'pk': product.pk}))

def test_remove_from_favorites_redirection(response_remove_from_favorites, product):
    assertRedirects(response_remove_from_favorites, reverse('core:product', kwargs={'pk': product.pk}))

def test_product_not_in_favorites(response_remove_from_favorites, product):
    assert product.baseproduct_ptr not in User.objects.first().favorites.all()
