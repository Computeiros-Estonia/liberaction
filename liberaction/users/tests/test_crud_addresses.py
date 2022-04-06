import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from liberaction.users.models import User

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
#@pytest.fixture
#def create_address_response(client, user):
#    client.force_login(user)
#    return client.post(reverse('create_address'), data={

#    })

#def test_create_address_status_code(create_address_response):
#    assert create_address_response.status_code == 200


# Read


# Update


# Delete
