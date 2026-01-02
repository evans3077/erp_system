from django.db import models
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    custodian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="custodian_stores"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
