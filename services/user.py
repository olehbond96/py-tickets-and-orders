from django.db.models.query import QuerySet
from db.models import User


def get_user_by_username(username: str) -> User:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username {username!r} not found")


def create_user(
    username: str,
    email: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
) -> User:
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )


def update_user(user_id: int, **kwargs) -> User:
    user = User.objects.get(id=user_id)
    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))
    for attr, value in kwargs.items():
        setattr(user, attr, value)
    user.save()
    return user


def get_users() -> QuerySet[User]:
    return User.objects.all().order_by("username")


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)
