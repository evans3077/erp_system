from django.core.exceptions import ValidationError
from django.db import transaction
from .models import StockItem, StockReceipt, StockRequest
from .cache import StockCacheService


class StockService:

    @staticmethod
    @transaction.atomic
    def receive_stock(store, item, quantity, added_by, received_by):
        stock_item, created = StockItem.objects.get_or_create(
            store=store,
            item=item,
            defaults={"quantity": 0}
        )
        stock_item.quantity += quantity
        stock_item.save()

        # Log the receipt
        StockReceipt.objects.create(
            store=store,
            item=item,
            quantity=quantity,
            added_by=added_by,
            received_by=received_by
        )

        # Update Redis cache
        StockCacheService.invalidate_stock(store.id, item.id)
        return stock_item

    @staticmethod
    def create_request(store, item, quantity, requested_by):
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        return StockRequest.objects.create(
            store=store,
            item=item,
            quantity=quantity,
            requested_by=requested_by
        )

    @staticmethod
    def approve_request(request_obj, approved_by):
        if request_obj.status != "pending":
            raise ValidationError("Request already processed.")

        request_obj.status = "approved"
        request_obj.approved_by = approved_by
        request_obj.save()
        return request_obj

    @staticmethod
    @transaction.atomic
    def issue_request(request_obj, issued_by):
        if request_obj.status != "approved":
            raise ValidationError("Request must be approved before issuing.")

        stock_item = StockItem.objects.get(
            store=request_obj.store,
            item=request_obj.item
        )

        if stock_item.quantity < request_obj.quantity:
            raise ValidationError("Not enough stock to issue.")

        stock_item.quantity -= request_obj.quantity
        stock_item.save()

        request_obj.status = "issued"
        request_obj.issued_by = issued_by
        request_obj.save()

        StockCacheService.invalidate_stock(stock_item.store.id, stock_item.item.id)
        return request_obj
