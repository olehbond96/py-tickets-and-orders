from typing import List, Dict, Any, Optional
from django.db import transaction
from django.shortcuts import get_object_or_404
from .user import get_user
from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet


@transaction.atomic
def create_order(
    tickets: List[Dict[str, Any]],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = get_user(username)
    order_data = {"user": user}
    if date:
        order_data["created_at"] = date

    order = Order.objects.create(**order_data)

    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        movie_session = get_object_or_404(MovieSession, pk=movie_session_id)

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data.get("row"),
            seat=ticket_data.get("seat")
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        user = get_user(username)
        orders = orders.filter(user=user)
    return orders
