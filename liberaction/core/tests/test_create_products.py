import os
from pathlib import Path
import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.contrib.auth.models import User
from django.urls import reverse

from liberaction.core.models import Album, Product, Tag

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create(username='root', password='toor')

# GET
@pytest.fixture
def create_product_request(client, user):
    client.force_login(user)
    return client.get(reverse('core:create_product'))

def test_create_product_status_code(create_product_request):
    assert create_product_request.status_code == 200

def test_form_present(create_product_request):
    form = create_product_request.context['form']
    for field in form:
        assertContains(create_product_request, f'id="id_{field.name}"')
    assertContains(create_product_request, f'<form action="{reverse("core:create_product")}"')

def test_submit_btn_present(create_product_request):
    assertContains(create_product_request, f'<button type="submit"')

# POST
# Fixtures
@pytest.fixture
def tags(client, db):
    return [
        Tag.objects.create(name='Software Development'),
        Tag.objects.create(name='UX Design'),
    ]

@pytest.fixture
def create_product_post(client, user, tags):
    img_path = Path(__file__).resolve().parent / 'images'
    images = os.listdir(img_path)
    img_list = []
    for img_name in images:
        img = open(os.path.join(img_path, img_name), 'rb')
        img_list.append(img)
        
    client.force_login(user)
    return client.post(reverse('core:create_product'), data={
        'name': 'Web Development',
        'tags': [t.id for t in tags],
        'owner': user.id,
        'description': 'Awesome stuff.',
        'images': img_list,
    })

# For debugging purposes, do not uncomment
# def test_form_is_valid(create_product_post):
#     assert not create_product_post.context['form'].errors

def test_create_product_status_code(create_product_post):
    assertRedirects(create_product_post, reverse('core:create_product'))

def test_product_exists(create_product_post):
    assert Product.objects.exists()

def test_album_exists(create_product_post):
    assert Album.objects.exists()