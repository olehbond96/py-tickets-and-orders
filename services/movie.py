from datetime import date
from django.db.models.query import QuerySet
from db.models import MovieSession


def get_movie_sessions(
    date: date = None,
    movie_id: int = None,
    cinema_hall_id: int = None,
) -> QuerySet[MovieSession]:
    queryset = MovieSession.objects.all()

    if date:
        queryset = queryset.filter(show_time__date=date)
    if movie_id:
        queryset = queryset.filter(movie_id=movie_id)
    if cinema_hall_id:
        queryset = queryset.filter(cinema_hall_id=cinema_hall_id)

    return queryset.order_by("show_time")


def create_movie_session(
    show_time: str, movie_id: int, cinema_hall_id: int
) -> MovieSession:
    return MovieSession.objects.create(
        show_time=show_time,
        movie_id=movie_id,
        cinema_hall_id=cinema_hall_id,
    )
