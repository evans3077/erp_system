from django.db import models
from accounts.models import User, Department

class Store(models.Model):
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    custodian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="store_custodian")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="store_manager")

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class Item(models.Model):
    name = models.CharField(max_length=200)
    is_returnable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=50)  # litres, pieces, kg etc.

    def __str__(self):
        return f"{self.item.name} @ {self.store.name}"
