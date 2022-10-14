import os
import pytest
from pathlib import Path
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

from liberaction.core.models import Album, Picture, Product, Tag

# Create

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
        assertContains(create_product_request, f'name="{field.name}"')
    assertContains(create_product_request, f'<form action="{reverse("core:create_product")}"')

def test_submit_btn_present(create_product_request):
    assertContains(create_product_request, f'<button type="submit"')

# POST
@pytest.fixture
def tags(client, db):
    return [
        Tag.objects.create(name='Software Development'),
        Tag.objects.create(name='UX Design'),
    ]

@pytest.fixture
def create_product_post(client, user, tags):
    # Create img list
    img_path = Path(__file__).resolve().parent / 'images'
    images = os.listdir(img_path)
    img_list = []
    for img_name in images:
        img = open(os.path.join(img_path, img_name), 'rb')
        img_list.append(img)
    # Response
    client.force_login(user)
    return client.post(reverse('core:create_product'), data={
        'name': 'Web Development',
        'tags': [t.id for t in tags],
        'owner': user.id,
        'description': 'Awesome stuff.',
        'price': 1000,
        'images': img_list,
        'is_new': True,
    })

# For debugging purposes only, do not uncomment
# def test_product_form_is_valid(create_product_post):
#     assert not create_product_post.context['form'].errors

def test_create_product_redirection(create_product_post):
    assertRedirects(create_product_post, reverse('core:index'))

def test_product_exists(create_product_post):
    assert Product.objects.exists()

def test_album_exists(create_product_post):
    assert Album.objects.exists()


# Read
@pytest.fixture
def product(user):
    return Product.objects.create(
        name='Web dev',
        owner=user,
        description='Coll stuff',
        price=10000
    )

@pytest.fixture
def pictures(product):
    album = Album.objects.create(base_product=product)
    return [
        Picture.objects.create(img='test/pic1.jpg', index=0, album=album),
        Picture.objects.create(img='test/pic2.jpg', index=1, album=album),
    ]

# GET
@pytest.fixture
def get_product_response(client, product, pictures):
    return client.get(
        reverse('core:product',
        kwargs={'pk': product.id})
    )

def test_product_page_status_code(get_product_response):
    assert get_product_response.status_code == 200

def test_product_present(get_product_response, product):
    assertContains(get_product_response, product.name)
    assertContains(get_product_response, product.price)
    assertContains(get_product_response, product.description)

def test_product_img_present(get_product_response, product):
    for pic in product.get_pictures():
        assertContains(get_product_response, pic.img.url)


# Update
@pytest.fixture
def get_edit_product(client, product, user, tags):
    client.force_login(user)
    return client.get(reverse('core:edit_product', kwargs={'pk':product.pk}))

def test_edit_product_status_code(get_edit_product):
    assert get_edit_product.status_code == 200

def test_edit_form_present(get_edit_product, product):
    form = get_edit_product.context['form']
    for field in form:
        assertContains(get_edit_product, f'name="{field.name}"')
    assertContains(get_edit_product, f'<form action="{reverse("core:edit_product", kwargs={"pk":product.pk})}"')

def test_edit_submit_btn_present(get_edit_product):
    assertContains(get_edit_product, f'<button type="submit"')

@pytest.fixture
def post_edit_product(client, product, user, tags):
    client.force_login(user)
    return client.post(reverse('core:edit_product', kwargs={'pk':product.pk}), data={
        'name': 'Web Development',
        'tags': [t.id for t in tags],
        'owner': user.id,
        'description': 'Awesome stuff.',
        'price': 1,
        'images': '',
        'is_new': True,
    })

def test_edit_product_redirection(post_edit_product, product):
    assertRedirects(post_edit_product, reverse('core:product', kwargs={'pk':product.pk}))

def test_product_edited(post_edit_product):
    assert Product.objects.first().price == 1


# Delete
@pytest.fixture
def post_delete_product(client, product, user):
    client.force_login(user)
    return client.post(reverse('core:delete_product', kwargs={'pk':product.pk}))

def test_delete_product_redirection(post_delete_product, product):
    assertRedirects(post_delete_product, reverse('core:index'))

def test_product_deleted(post_delete_product):
    assert not Product.objects.exists()
