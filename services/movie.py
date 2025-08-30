from django.db.models.query import QuerySet
from db.models import Movie, Actor, Genre


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet[Movie]:

    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)
    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)
    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset


def create_movie(
    title: str,
    description: str,
    actors_ids: list[int],
    genres_ids: list[int],
) -> Movie:
    movie = Movie.objects.create(title=title, description=description)
    actors = Actor.objects.filter(id__in=actors_ids)
    genres = Genre.objects.filter(id__in=genres_ids)

    movie.actors.set(actors)
    movie.genres.set(genres)

    return movie
