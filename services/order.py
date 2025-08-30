from django.db.models.query import QuerySet
from datetime import datetime
from db.models import Order, Ticket, MovieSession, User


def get_orders(user_id: int = None, username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if user_id:
        queryset = queryset.filter(user_id=user_id)
    elif username:
        queryset = queryset.filter(user__username=username)

    return queryset.order_by("-created_at")


def create_order(
    tickets: list,
    username: str,
    date: str = None,
) -> Order:

    user = User.objects.get(username=username)

    if date:
        order_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        order_date = datetime.now()

    order = Order.objects.create(user=user, created_at=order_date)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order
