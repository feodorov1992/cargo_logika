"""
Django command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand

from logistics.models import Order


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        order = Order.objects.first()
        order.send_creation_email()
        order.send_creation_email('user')
