from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with id {user_id} not found.")


def get_users() -> list[User]:
    return list(User.objects.all())


@transaction.atomic
def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    user_data = {
        "username": username,
        "password": password,
    }
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    user = User.objects.create_user(**user_data)
    user.save()
    return user


@transaction.atomic
def update_user(
    user_id: int,
    username: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    """
    Updates a user with the given ID.
    """
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
    return user


@transaction.atomic
def delete_user(user_id: int) -> None:
    user = get_object_or_404(User, id=user_id)
    user.delete()
