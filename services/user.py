from typing import Optional
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


def get_user(user_id: int) -> get_user_model():
    User = get_user_model()
    return get_object_or_404(User, id=user_id)


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> get_user_model():
    User = get_user_model()
    optional_fields = {}
    if email:
        optional_fields['email'] = email
    if first_name:
        optional_fields['first_name'] = first_name
    if last_name:
        optional_fields['last_name'] = last_name

    return User.objects.create_user(
        username=username,
        password=password,
        **optional_fields
    )


@transaction.atomic
def update_user(
        user_id: int,
        email: Optional[str] = None,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> get_user_model():
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
