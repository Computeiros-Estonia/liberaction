import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from liberaction.users.models import User

# GET
@pytest.fixture
def resposta_register_get(client, db):
    return client.get(reverse('register'))

def test_register_status_code(resposta_register_get):
    assert resposta_register_get.status_code == 200

def test_form_present(resposta_register_get):
    assertContains(resposta_register_get, f'<form action="{reverse("register")}" method="POST"')

def test_all_genders_present(resposta_register_get):
    for gender in User.GENDER_CHOICES:
        assertContains(resposta_register_get, gender[1])

def test_btn_submit_present(resposta_register_get):
    assertContains(resposta_register_get, '<button type="submit"')

# POST
data = {
    'email': 'root@liberaction.com.br',
    'first_name' : 'Root',
    'last_name' : 'User',
    'gender' : 'm',
    'cpf': '00000000000',
    'password1': 'testingUser123',
    'password2': 'testingUser123',
    'birth_date': '1999-01-01 02:00:00+00:00',
}

@pytest.fixture
def resposta_register_post(client, db):
    return client.post(reverse('register'), data=data)


# def test_sem_erros(resposta_register_post):
#     assert not resposta_register_post.context['form'].errors

def test_register_redirection(resposta_register_post):
    assertRedirects(resposta_register_post, reverse('core:index'))

def test_user_exists(resposta_register_post):
    assert User.objects.exists()

def test_user_autenticated(resposta_register_post):
    assert resposta_register_post.wsgi_request.user.is_authenticated == True

def test_user_atts_posted(resposta_register_post):
    cleaned_data = data
    cleaned_data.pop('password1')
    cleaned_data.pop('password2')
    for k,v in data.items():
        assert str(User.objects.first().__getattribute__(k)) == v
