import os
from pathlib import Path
import pytest
from pytest_django.asserts import assertContains, assertRedirects
from liberaction.users.models import User
from django.urls import reverse

from liberaction.core.models import Album, BaseProduct, Picture, Product, Tag

# Create
@pytest.fixture
def user(db):
    return User.objects.create(email='root@liberaction.com.br', password='toor')

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
        assertContains(create_product_request, f'name="base-{field.name}"')
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
        'base-name': 'Web Development',
        'base-tags': [t.id for t in tags],
        'base-owner': user.id,
        'base-description': 'Awesome stuff.',
        'base-price': 1000,
        'base-images': img_list,
        'product-is_new': True,
    })

# For debugging purposes only, do not uncomment
# def test_base_form_is_valid(create_product_post):
#     assert not create_product_post.context['base_form'].errors

# def test_product_form_is_valid(create_product_post):
#     assert not create_product_post.context['product_form'].errors

def test_create_product_redirection(create_product_post):
    assertRedirects(create_product_post, reverse('core:create_product'))

def test_base_product_exists(create_product_post):
    assert BaseProduct.objects.exists()

def test_product_exists(create_product_post):
    assert Product.objects.exists()

def test_album_exists(create_product_post):
    assert Album.objects.exists()


# Read
@pytest.fixture
def product(user):
    base = BaseProduct.objects.create(
        name='Web dev',
        owner=user,
        description='Coll stuff',
        price=10000
    )
    return Product.objects.create(base=base)

@pytest.fixture
def pictures(product):
    album = Album.objects.create(base_product=product.base)
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
    assertContains(get_product_response, product.base.name)
    assertContains(get_product_response, product.base.owner)
    assertContains(get_product_response, product.base.description)

def test_product_img_present(get_product_response, product):
    for pic in product.base.get_pictures():
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
        assertContains(get_edit_product, f'name="base-{field.name}"')
    assertContains(get_edit_product, f'<form action="{reverse("core:edit_product", kwargs={"pk":product.pk})}"')

def test_edit_submit_btn_present(get_edit_product):
    assertContains(get_edit_product, f'<button type="submit"')

@pytest.fixture
def post_edit_product(client, product, user, tags):
    client.force_login(user)
    return client.post(reverse('core:edit_product', kwargs={'pk':product.pk}), data={
        'base-name': 'Web Development',
        'base-tags': [t.id for t in tags],
        'base-owner': user.id,
        'base-description': 'Awesome stuff.',
        'base-price': 1,
        'base-images': '',
        'product-is_new': True,
    })

def test_edit_product_redirection(post_edit_product, product):
    assertRedirects(post_edit_product, reverse('core:product', kwargs={'pk':product.pk}))

def test_product_edited(post_edit_product):
    assert Product.objects.first().get_price() == 1


# Delete
@pytest.fixture
def post_delete_product(client, product, user):
    client.force_login(user)
    return client.post(reverse('core:delete_product', kwargs={'pk':product.pk}))

def test_delete_product_redirection(post_delete_product, product):
    assertRedirects(post_delete_product, reverse('core:index'))

def test_product_deleted(post_delete_product):
    assert not Product.objects.exists()
