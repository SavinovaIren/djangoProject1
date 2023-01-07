import pytest


@pytest.mark.django_db
def test_user_create(client, django_user_model):
    """create user tests"""
    data = {
        "username": "test user",
        "password": "ytyukjkgh",
        "password_repeat": "ytyukjkgh",
    }

    response = client.post(
        path="/core/signup",
        data=data,
        content_type="application/json"
    )

    user = django_user_model.objects.last()

    assert response.status_code == 201
    assert response.data == {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }

