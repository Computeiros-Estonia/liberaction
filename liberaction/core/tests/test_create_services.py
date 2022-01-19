import os
from pathlib import Path
import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.contrib.auth.models import User
from django.urls import reverse

from liberaction.core.models import Album, BaseProduct, Service, Tag

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create(username='root', password='toor')

# GET
@pytest.fixture
def create_service_request(client, user):
    client.force_login(user)
    return client.get(reverse('core:create_service'))

def test_create_service_status_code(create_service_request):
    assert create_service_request.status_code == 200

def test_form_present(create_service_request):
    form = create_service_request.context['form']
    for field in form:
        assertContains(create_service_request, f'name="base-{field.name}"')
    assertContains(create_service_request, f'<form action="{reverse("core:create_service")}"')

def test_submit_btn_present(create_service_request):
    assertContains(create_service_request, f'<button type="submit"')

# POST
# Fixtures
@pytest.fixture
def tags(client, db):
    return [
        Tag.objects.create(name='Software Development'),
        Tag.objects.create(name='UX Design'),
    ]

@pytest.fixture
def create_service_post(client, user, tags):
    # Create img list
    img_path = Path(__file__).resolve().parent / 'images'
    images = os.listdir(img_path)
    img_list = []
    for img_name in images:
        img = open(os.path.join(img_path, img_name), 'rb')
        img_list.append(img)
    # Response
    client.force_login(user)
    return client.post(reverse('core:create_service'), data={
        'base-name': 'Web Development',
        'base-tags': [t.id for t in tags],
        'base-owner': user.id,
        'base-description': 'Awesome stuff.',
        'base-price': 1000,
        'base-images': img_list,
        'service-is_negotiable': False,
    })

# For debugging purposes, do not uncomment
# def test_base_form_is_valid(create_service_post):
#     assert not create_service_post.context['base_form'].errors

# def test_service_form_is_valid(create_service_post):
#     assert not create_service_post.context['service_form'].errors

def test_create_service_redirection(create_service_post):
    assertRedirects(create_service_post, reverse('core:create_service'))

def test_base_service_exists(create_service_post):
    assert BaseProduct.objects.exists()

def test_service_exists(create_service_post):
    assert Service.objects.exists()

def test_album_exists(create_service_post):
    assert Album.objects.exists()