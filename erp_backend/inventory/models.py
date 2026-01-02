from django.db import models
from django.conf import settings

# -------------------------
# Store and Inventory Models
# -------------------------
class Store(models.Model):
    name = models.CharField(max_length=150, unique=True)
    location = models.CharField(max_length=255, blank=True)
    custodian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stores_managed"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=50)  # e.g., kg, litre, piece
    is_returnable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="store_items"
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="store_items"
    )
    quantity = models.FloatField(default=0)

    class Meta:
        unique_together = ("store", "item")

    def __str__(self):
        return f"{self.store.name} - {self.item.name}: {self.quantity}"


# -------------------------
# Stock Movements (In/Out)
# -------------------------
class StockMovement(models.Model):
    MOVEMENT_TYPE = [
        ("receipt", "Receipt"),  # incoming stock
        ("issue", "Issue"),      # outgoing stock
        ("return", "Return")     # returned stock
    ]

    store_item = models.ForeignKey(
        StoreItem,
        on_delete=models.CASCADE,
        related_name="movements"
    )
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE)
    quantity = models.FloatField()
    done_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stock_movements"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.movement_type.capitalize()} {self.quantity} {self.store_item.item.unit} of {self.store_item.item.name}"


# -------------------------
# Stock Requests
# -------------------------
class StockRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Manager Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("issued", "Issued"),
    ]

    store_item = models.ForeignKey(
        StoreItem,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    quantity = models.FloatField()
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="requests_made"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests_approved"
    )
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests_issued"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_item.item.name} ({self.quantity}) - {self.status}"


# -------------------------
# Issue and Return Vouchers
# -------------------------
class IssueVoucher(models.Model):
    stock_request = models.OneToOneField(
        StockRequest,
        on_delete=models.CASCADE,
        related_name="issue_voucher"
    )
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="issue_vouchers"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IssueVoucher #{self.id} for {self.stock_request.store_item.item.name}"


class ReturnVoucher(models.Model):
    stock_movement = models.OneToOneField(
        StockMovement,
        on_delete=models.CASCADE,
        related_name="return_voucher"
    )
    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="return_vouchers"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReturnVoucher #{self.id} for {self.stock_movement.store_item.item.name}"
