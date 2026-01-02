from rest_framework import serializers
from .models import Store, Item, StockItem, StockReceipt, StockRequest


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = "__all__"


class StockReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReceipt
        fields = "__all__"


class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequest
        fields = "__all__"
