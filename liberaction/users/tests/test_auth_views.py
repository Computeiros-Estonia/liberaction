import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse

# GET login
@pytest.fixture
def resposta_login_get(client, db):
    return client.get(reverse('login'))

def test_login_status_code(resposta_login_get):
    assert resposta_login_get.status_code == 200

def test_form_present(resposta_login_get):
    assertContains(resposta_login_get, f'<form action="{reverse("login")}" method="POST"')

def test_btn_submit_present(resposta_login_get):
    assertContains(resposta_login_get, '<button type="submit"')

# POST login
@pytest.fixture
def user(db):
    return User.objects.create_user(username='root', password='testingUser123')

@pytest.fixture
def resposta_login_post(client, user):
    return client.post(reverse('login'), data={
        'username': 'root',
        'password': 'testingUser123',
    })

def test_user_autenticated(resposta_login_post):
    assert resposta_login_post.wsgi_request.user.is_authenticated == True

def test_login_post_redirection(resposta_login_post):
    assertRedirects(resposta_login_post, reverse('core:index'))

# logout
@pytest.fixture
def resposta_logout(client, user):
    client.force_login(user)
    return client.get(reverse('logout'))

def test_user_not_autenticated(resposta_logout):
    assert resposta_logout.wsgi_request.user.is_authenticated == False

def test_logout_post_redirection(resposta_logout):
    assertRedirects(resposta_logout, reverse('core:index'))
