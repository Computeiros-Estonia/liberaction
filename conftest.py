import pytest
from liberaction.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create(email='root@liberaction.com.br', password='toor')
