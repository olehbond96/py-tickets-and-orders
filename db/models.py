from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.core.exceptions import ValidationError


class User(AbstractUser, PermissionsMixin):
    date_of_birth = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name="db_users",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="db_users_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", related_name="movies")
    genres = models.ManyToManyField("Genre", related_name="movies")
    release_date = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name="sessions")

    def __str__(self):
        return f"{self.movie.title} at {self.show_time}"


class Order(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Order: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}>"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    movie_session = models.ForeignKey(
        "MovieSession", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_movie_session_row_seat",
            )
        ]

    def __str__(self):
        return (
            f"<Ticket: {self.movie_session.movie.title} "
            f"{self.movie_session.show_time} (row: {self.row}, seat: {self.seat})>"
        )

    def clean(self):
        if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError(
                {"row": [
                    "row number must be in available range: "
                    f"(1, {self.movie_session.cinema_hall.rows})"
                ]}
            )

        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError(
                {"seat": [
                    "seat number must be in available range: "
                    f"(1, {self.movie_session.cinema_hall.seats_in_row})"
                ]}
            )
