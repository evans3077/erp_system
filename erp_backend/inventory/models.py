from django.db import models
from accounts.models import User
from stores.models import Store, Item

MOVEMENT_TYPES = [
    ("ADD", "Add Items"),
    ("RECEIVE", "Receive Items"),
    ("REQUEST", "Request Items"),
    ("APPROVE", "Approve Request"),
    ("ISSUE", "Issue Items"),
]

class InventoryMovement(models.Model):
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approved_movements", blank=True)
    request_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="requested_movements", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.item.name} - {self.quantity}"
