from django.db import models


class Item(models.Model):
    """
    Represents an inventory item.
    All items are countable (no weights, no units like kg/litre).
    Examples: Chairs, Microphones, Pens, Detergent bottles, Tents, etc.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # Category helps filtering 
    category = models.CharField(max_length=255)

    # Minimum level before alerts
    reorder_level = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
