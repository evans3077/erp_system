from django.contrib import admin
from .models import Store, Item, StoreItem, StockMovement, StockRequest, IssueVoucher, ReturnVoucher


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "custodian", "location", "created_at")
    search_fields = ("name",)
    list_filter = ("custodian",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "is_returnable")
    search_fields = ("name",)


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ("store", "item", "quantity")
    search_fields = ("store__name", "item__name")
    list_filter = ("store",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("store_item", "movement_type", "quantity", "done_by", "timestamp")
    list_filter = ("movement_type", "timestamp")
    search_fields = ("store_item__store__name", "store_item__item__name")


@admin.register(StockRequest)
class StockRequestAdmin(admin.ModelAdmin):
    list_display = ("store_item", "quantity", "status", "requested_by", "approved_by", "issued_by", "timestamp")
    list_filter = ("status",)
    search_fields = ("store_item__item__name", "requested_by__username")


@admin.register(IssueVoucher)
class IssueVoucherAdmin(admin.ModelAdmin):
    list_display = ("stock_request", "issued_by", "timestamp")
    search_fields = ("stock_request__store_item__item__name", "issued_by__username")
    list_filter = ("issued_by",)


@admin.register(ReturnVoucher)
class ReturnVoucherAdmin(admin.ModelAdmin):
    list_display = ("stock_movement", "returned_by", "timestamp")
    search_fields = ("stock_movement__store_item__item__name", "returned_by__username")
    list_filter = ("returned_by",)
