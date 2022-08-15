import os
import pytest
from pathlib import Path
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from liberaction.core.models import Album, BaseProduct, Service, Tag

# Create
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

# For debugging purposes only, do not uncomment
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

# Read
@pytest.fixture
def service(user):
    base = BaseProduct.objects.create(
        name='Web dev',
        owner=user,
        description='Coll stuff',
        price=10000
    )
    return Service.objects.create(base=base)

# GET
@pytest.fixture
def get_service_response(client, service):
    return client.get(
        reverse('core:service',
        kwargs={'pk': service.id})
    )

def test_service_page_status_code(get_service_response):
    assert get_service_response.status_code == 200

def test_service_present(get_service_response, service):
    assertContains(get_service_response, service.base.name)
    assertContains(get_service_response, service.base.owner)
    assertContains(get_service_response, service.base.description)


# Update
@pytest.fixture
def get_edit_service(client, service, user, tags):
    client.force_login(user)
    return client.get(reverse('core:edit_service', kwargs={'pk':service.pk}))

def test_edit_service_status_code(get_edit_service):
    assert get_edit_service.status_code == 200

def test_edit_form_present(get_edit_service, service):
    form = get_edit_service.context['form']
    for field in form:
        assertContains(get_edit_service, f'name="base-{field.name}"')
    assertContains(get_edit_service, f'<form action="{reverse("core:edit_service", kwargs={"pk":service.pk})}"')

def test_edit_submit_btn_present(get_edit_service):
    assertContains(get_edit_service, f'<button type="submit"')

@pytest.fixture
def post_edit_service(client, service, user, tags):
    client.force_login(user)
    return client.post(reverse('core:edit_service', kwargs={'pk':service.pk}), data={
        'base-name': 'Web Development',
        'base-tags': [t.id for t in tags],
        'base-owner': user.id,
        'base-description': 'Awesome stuff.',
        'base-price': 1,
        'base-images': '',
        'service-is_new': True,
    })

def test_edit_service_redirection(post_edit_service, service):
    assertRedirects(post_edit_service, reverse('core:service', kwargs={'pk':service.pk}))

def test_service_edited(post_edit_service):
    assert Service.objects.first().get_price() == 1


# Delete
@pytest.fixture
def post_delete_service(client, service, user):
    client.force_login(user)
    return client.post(reverse('core:delete_service', kwargs={'pk':service.pk}))

def test_delete_service_redirection(post_delete_service, service):
    assertRedirects(post_delete_service, reverse('core:index'))

def test_service_deleted(post_delete_service):
    assert not Service.objects.exists()
