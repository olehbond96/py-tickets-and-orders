from datetime import datetime
from typing import List
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.user import get_user
from services.movie_session import get_movie_session
from services.ticket import get_ticket


def get_orders(user_id: int) -> QuerySet[Order]:
    return Order.objects.filter(user_id=user_id).order_by("-order_date")


@transaction.atomic
def create_order(user_id: int, ticket_ids: List[int]) -> Order:
    user = get_user(user_id)
    tickets = Ticket.objects.filter(id__in=ticket_ids).select_related(
        "movie_session"
    )

    if tickets.count() != len(ticket_ids):
        raise ValueError("Some tickets were not found.")

    for ticket in tickets:
        if ticket.order:
            raise ValueError(f"Ticket {ticket.id} is already ordered.")

    order = Order.objects.create(user=user, order_date=datetime.now())

    for ticket in tickets:
        ticket.order = order
        ticket.save()
    return order
