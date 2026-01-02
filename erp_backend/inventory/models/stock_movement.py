from django.db import models
from django.contrib.auth import get_user_model
from .store import Store
from .item import Item

User = get_user_model()

class StockMovement(models.Model):
    # Used when stock is taken from a store
    source_store = models.ForeignKey(
        Store,
        related_name="outgoing_movements",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Used when stock is delivered to a store
    destination_store = models.ForeignKey(
        Store,
        related_name="incoming_movements",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

   
    store = models.ForeignKey(
        Store,
        related_name="general_movements",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

   
