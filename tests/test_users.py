from app import schemas
from jose import jwt
import pytest
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get(
        'message') == "Welcome to my API !! -> Add '/docs' to the end of the url to go to the API documentation"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    # When we add the output to a schema, Pydantic model validates it. If there is an Exception, Pytest will display it
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('testemail@gmail.com', 'wrongPassword', 403),
    ('wrongemail@gmail.com', 'wrongPassword', 403),
    (None, 'password123', 422),
    ('testemail@gmail.com', None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
