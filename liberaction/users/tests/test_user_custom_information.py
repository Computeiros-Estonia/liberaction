import pytest
from liberaction.users.models import User, PhoneNumber, Address

@pytest.fixture
def user(db):
    return User.objects.create(email='root@liberaction.com.br', password='toor')

def test_user_exists(user):
    assert User.objects.exists()

@pytest.fixture
def phone_number(user):
    return PhoneNumber.objects.create(
        user=user, ddi=55, ddd=11,
        number=999999999, is_main=True
    )

def test_phone_number_exists(phone_number):
    assert PhoneNumber.objects.exists()

@pytest.fixture
def address(user):
    return Address.objects.create(
        user=user, country='Brasil',
        state='SP', city='Sao Paulo',
        address1='Av. Do Lado De La',
        cep='04613-030', is_main=True
    )

def test_address_exists(address):
    assert Address.objects.exists()
