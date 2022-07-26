import pytest
from django.urls import reverse
from django.contrib.sessions.models import Session
from liberaction.core.models import BaseProduct, Product
from liberaction.users.models import User

@pytest.fixture
def user(db):
    return User.objects.create(email='root@liberaction.com.br', password='toor')

@pytest.fixture
def product(user):
    base = BaseProduct.objects.create(
        name='Web dev',
        owner=user,
        description='Coll stuff',
        price=10000
    )
    return Product.objects.create(base=base)

@pytest.fixture
def response(client, user, product):
    client.force_login(user)
    return client.post(reverse('basket:basket_add'), data={
        'product_id': product.id,
        'product_qty': 2,
    })

def test_product_in_basket(response, product):
    session = Session.objects.get(pk=response.get('sessionid'))
    assert product.id in session.get('basket')