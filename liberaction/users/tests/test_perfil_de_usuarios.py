import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from liberaction.users.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(email='root@liberaction.com.br', password='testingUser123')

@pytest.fixture
def resposta_get_perfil(client, user):
    client.force_login(user)
    return client.get(reverse('perfil'))

def test_get_perfil_status_code(resposta_get_perfil):
    assert resposta_get_perfil.status_code == 200

@pytest.fixture
def resposta_post_perfil(client, user):
    client.force_login(user)
    return client.post(reverse('perfil'), data={
        'email': 'root@liberaction.com.br',
        'first_name': 'Root',
        'last_name': 'User',
        'cpf': '00000000000',
    })

def test_post_perfil_redirection(resposta_post_perfil):
    assertRedirects(resposta_post_perfil, reverse('perfil'))

def test_perfil_changed(resposta_post_perfil):
    assert User.objects.first().first_name == 'Root'
