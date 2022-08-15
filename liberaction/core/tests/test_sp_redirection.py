# This tests the page for service vs. product redirection
import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains


@pytest.fixture
def response_sp_redirection(client, user):
    client.force_login(user)
    return client.get(reverse('core:sp_redirection'))

def test_status_code(response_sp_redirection):
    assert response_sp_redirection.status_code == 200

def test_btn_new_product_exists(response_sp_redirection):
    assertContains(response_sp_redirection, f'<a href="{reverse("core:create_product")}"')

def test_btn_new_service_exists(response_sp_redirection):
    assertContains(response_sp_redirection, f'<a href="{reverse("core:create_service")}"')
