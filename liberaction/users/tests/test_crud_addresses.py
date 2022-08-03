import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from liberaction.users.models import Address, User

# Create
@pytest.fixture
def user(db):
    return User.objects.create_user(email='root@liberaction.com.br', password='testingUser123')

# GET
@pytest.fixture
def create_address_response(client, user):
    client.force_login(user)
    return client.get(reverse('create_address'))

def test_create_address_status_code(create_address_response):
    assert create_address_response.status_code == 200

def test_create_address_form_present(create_address_response):
    assertContains(create_address_response, f'<form action="{reverse("create_address")}" method="POST"')

def test_create_address_submit_btn_present(create_address_response):
    assertContains(create_address_response, '<button type="submit"')

# POST
@pytest.fixture
def create_address_post_response(client, user):
   client.force_login(user)
   return client.post(reverse('create_address'), data={
        'country': 'Brasil',
        'state': 'SP',
        'city': 'São Paulo',
        'neighborhood': 'Campo Belo',
        'address1': 'R. Republica do Iraque, 240',
        'address2': 'Bloco B, ap. 21',
        'cep': '04613-030',
        'is_main': 'True',
   })

def test_create_address_redirection(create_address_post_response):
    user = User.objects.first()
    assertRedirects(create_address_post_response, reverse('user_addresses', kwargs={'user_pk': user.pk}))

def test_address_created(create_address_post_response):
    assert Address.objects.exists()


# Read
@pytest.fixture
def addresses(user):
    return [
        Address.objects.create(user=user, country='Brasil', state='SP', city='São Paulo', address1='R. Republica do Iraque, 240', cep='04613-030'),
        Address.objects.create(user=user, country='Brasil', state='SP', city='São Paulo', address1='R. Lapa lá, 309', cep='04613-030'),
    ]

@pytest.fixture
def read_addresses_response(client, user, addresses):
    client.force_login(user)
    return client.get(reverse('user_addresses', kwargs={'user_pk': user.pk}))

def test_read_addresses_status_code(read_addresses_response):
    assert read_addresses_response.status_code == 200

def test_all_addresses_present(read_addresses_response):
    addresses = Address.objects.all()
    for ad in addresses:
        assertContains(read_addresses_response, ad)


# Update

# GET
@pytest.fixture
def update_address_response(client, user, addresses):
    client.force_login(user)
    return client.get(reverse('update_address', kwargs={'pk': addresses[0].pk}))

def test_update_addresses_status_code(update_address_response):
    assert update_address_response.status_code == 200

def test_update_address_form_present(update_address_response):
    address = Address.objects.first()
    assertContains(update_address_response,
        f'<form action="{reverse("update_address", kwargs={"pk": address.pk})}" method="POST"')

def test_update_address_submit_btn_present(update_address_response):
    assertContains(update_address_response, '<button type="submit"')


# POST
@pytest.fixture
def update_address_post_response(client, user, addresses):
   client.force_login(user)
   return client.post(reverse('update_address', kwargs={"pk": addresses[0].pk}), data={
        'country': 'Brasil',
        'state': 'SP',
        'city': 'São Paulo',
        'neighborhood': 'Campo Belo',
        'address1': 'R. Republica do Iraque, 240',
        'address2': 'Bloco B, ap. 21',
        'cep': '04613-031',
        'is_main': 'True',
   })

def test_update_address_redirection(update_address_post_response):
    user = User.objects.first()
    assertRedirects(update_address_post_response, reverse('user_addresses', kwargs={'user_pk': user.pk}))

def test_address_updated(update_address_post_response):
    assert Address.objects.first().cep == '04613-031'


# Delete
@pytest.fixture
def delete_address_response(client, user, addresses):
   client.force_login(user)
   return client.post(reverse('delete_address', kwargs={"pk": addresses[0].pk}))

def test_delete_address_redirection(delete_address_response):
    user = User.objects.first()
    assertRedirects(delete_address_response, reverse('user_addresses', kwargs={'user_pk': user.pk}))

def test_address_deleted(delete_address_response):
    assert len(Address.objects.all()) == 1

