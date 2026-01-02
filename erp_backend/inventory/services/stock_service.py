# inventory/services/stock_service.py

from django.db import transaction
from inventory.models import StoreItem, StockRequest, StockMovement
from inventory.services.cache_service import StockCacheService


class StockService:

    @staticmethod
    @transaction.atomic
    def issue_stock(request_obj: StockRequest, issued_by):
        """
        Issue items to the requester after approval.
        """
        store_item = request_obj.store_item

        if store_item.quantity < request_obj.quantity:
            raise ValueError("Not enough stock to issue.")

        # Reduce stock
        store_item.quantity -= request_obj.quantity
        store_item.save()

        # Invalidate cache
        StockCacheService.invalidate_stock(store_item.store.id, store_item.item.id)

        # Record movement
        movement = StockMovement.objects.create(
            store_item=store_item,
            movement_type="issue",
            quantity=request_obj.quantity,
            done_by=issued_by
        )

        # Update request status
        request_obj.status = "issued"
        request_obj.issued_by = issued_by
        request_obj.save()

        return movement
