from django.db import models


class Store(models.Model):
    """
    Represents a physical or logical store where items are stored..
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    #who is responsible for the store
    custodian = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stores_in_charge"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
