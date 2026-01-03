from rest_framework import serializers
from .models import Store, Item, StockRequest, StockMovement, StoreItem, IssueVoucher, ReturnVoucher

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class StoreItemSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = StoreItem
        fields = "__all__"

class StockMovementSerializer(serializers.ModelSerializer):
    store_item = StoreItemSerializer(read_only=True)
    done_by = serializers.StringRelatedField()
    
    class Meta:
        model = StockMovement
        fields = ["id", "store_item", "movement_type", "quantity", "done_by", "timestamp", "remarks"]






class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequest
        fields = "__all__"

class ReturnVoucherSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="stock_movement.store_item.item.name", read_only=True)
    store = serializers.CharField(source="stock_movement.store_item.store.name", read_only=True)
    quantity = serializers.FloatField(source="stock_movement.quantity", read_only=True)
    returned_by = serializers.CharField(source="returned_by.username", read_only=True)

    class Meta:
        model = ReturnVoucher
        fields = ["id", "store", "item", "quantity", "returned_by", "timestamp"]
