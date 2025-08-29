from typing import Optional
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.models import User


def get_user(user_id: int) -> User:
    user = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found")


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    user = get_user_model()

    user_data = {
        "username": username,
        "password": password
    }
    if email is not None:
        user_data["email"] = email
    if first_name is not None:
        user_data["first_name"] = first_name
    if last_name is not None:
        user_data["last_name"] = last_name

    return User.objects.create_user(**user_data)


def update_user(
        user_id: int,
        email: Optional[str] = None,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    user = get_user(user_id)

    if email is not None:
        user.email = email
    if password is not None:
        user.set_password(password)
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user
