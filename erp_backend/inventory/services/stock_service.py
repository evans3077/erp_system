# inventory/services/stock_service.py

from django.db import transaction
from inventory.models import StoreItem, StockRequest, StockMovement, ReturnVoucher
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

    @staticmethod
    @transaction.atomic
    def return_stock(movement_obj, returned_by, quantity=None):
    
        """
        Handle stock return.
        movement_obj: the original StockMovement that is being returned
        returned_by: the user returning the stock
        quantity: optional, if partial return
        """
        store_item = movement_obj.store_item
        return_qty = quantity or movement_obj.quantity

        # Add returned quantity back to stock
        store_item.quantity += return_qty
        store_item.save()

        # Invalidate cache
        StockCacheService.invalidate_stock(store_item.store.id, store_item.item.id)

        # Log the return as a StockMovement
        return_movement = StockMovement.objects.create(
            store_item=store_item,
            movement_type="return",
            quantity=return_qty,
            done_by=returned_by
        )

        # Create a ReturnVoucher record
        from inventory.models import ReturnVoucher
        ReturnVoucher.objects.create(
            stock_movement=return_movement,
            returned_by=returned_by
        )

        return return_movement
    


    @staticmethod
    @transaction.atomic
    def return_stock(store_item, quantity, returned_by):
        """
        Process returned items: update StoreItem, create StockMovement and ReturnVoucher
        """
        if quantity <= 0:
            raise ValueError("Return quantity must be positive.")

        # Update store item quantity
        store_item.quantity += quantity
        store_item.save()

        # Create stock movement record
        movement = StockMovement.objects.create(
            store_item=store_item,
            movement_type="return",
            quantity=quantity,
            done_by=returned_by
        )

        # Create ReturnVoucher
        voucher = ReturnVoucher.objects.create(
            stock_movement=movement,
            returned_by=returned_by
        )

        # Invalidate cache if you have caching
        StockCacheService.invalidate_stock(store_item.store.id, store_item.item.id)

        return voucher