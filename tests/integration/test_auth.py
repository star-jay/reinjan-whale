import pytest
from rest_framework.authtoken.models import Token

from tests.factories import UserFactory


@pytest.mark.django_db
def test_unauthorized(client):
    # Create a test user
    api_url = '/characters/'
    # Send a GET request to the protected endpoint
    response = client.get(api_url)
    # Assert that the response status code is 200
    assert response.status_code == 403


@pytest.mark.django_db
def test_authorized_with_token(client):
    user = UserFactory()
    # Create a token for the user
    token = Token.objects.create(user=user)
    api_url = '/characters/'
    # Set the token in the Authorization header
    headers = {'HTTP_AUTHORIZATION': f'Token {token.key}'}
    # Send a GET request to the protected endpoint
    response = client.get(api_url, **headers)
    # Assert that the response status code is 200
    assert response.status_code == 200
