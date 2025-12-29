from django.db import transaction
from stores.models import StoreItem
from inventory.models import InventoryMovement
from cache_service import StockCacheService

class InventoryService:

    @staticmethod
    @transaction.atomic
    def add_items(store, item, quantity, user):
        """Admin or custodian adds new items into the system."""
        movement = InventoryMovement.objects.create(
            movement_type="ADD",
            store=store,
            item=item,
            quantity=quantity,
            created_by=user
        )
        return movement

    @staticmethod
    @transaction.atomic
    def receive_items(store, item, quantity, created_by, approved_by):
        """Manager confirms items added by storekeeper."""
        store_item, _ = StoreItem.objects.get_or_create(
            store=store, item=item,
            defaults={"quantity": 0, "unit": "pcs"}
        )

        store_item.quantity += quantity
        store_item.save()

        StockCacheService.invalidate_stock(store.id, item.id)

        movement = InventoryMovement.objects.create(
            movement_type="RECEIVE",
            store=store,
            item=item,
            quantity=quantity,
            created_by=created_by,
            approved_by=approved_by
        )

        return movement

    @staticmethod
    @transaction.atomic
    def request_item(store, item, quantity, request_user):
        """Any user submits a request for an item."""
        movement = InventoryMovement.objects.create(
            movement_type="REQUEST",
            store=store,
            item=item,
            quantity=quantity,
            request_user=request_user,
        )
        return movement

    @staticmethod
    @transaction.atomic
    def approve_request(movement, manager_user):
        """Manager approves the request before issuing."""
        movement.movement_type = "APPROVE"
        movement.approved_by = manager_user
        movement.save()
        return movement

    @staticmethod
    @transaction.atomic
    def issue_item(store, item, quantity, created_by, approved_by):
        """Storekeeper issues items after approval."""
        store_item = StoreItem.objects.get(store=store, item=item)

        if store_item.quantity < quantity:
            raise ValueError("Not enough stock to issue.")

        store_item.quantity -= quantity
        store_item.save()

        StockCacheService.invalidate_stock(store.id, item.id)

        movement = InventoryMovement.objects.create(
            movement_type="ISSUE",
            store=store,
            item=item,
            quantity=quantity,
            created_by=created_by,
            approved_by=approved_by
        )

        return movement
