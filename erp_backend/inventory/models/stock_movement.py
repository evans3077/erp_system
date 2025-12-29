from django.db import models
from django.contrib.auth import get_user_model
from .store import Store
from .item import Item

User = get_user_model()

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ("ADD", "Add Stock"),
        ("REMOVE", "Remove Stock"),
        ("TRANSFER", "Transfer Stock"),
        ("ADJUST", "Adjust Stock"),  # Manual corrections
    )

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="movements")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="movements")

    # For transfers
    source_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name="outgoing_transfers")
    destination_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name="incoming_transfers")

    quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.movement_type} - {self.item.name} ({self.quantity})"
