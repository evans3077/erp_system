import json
from django.core.cache import cache
from .models import StockItem


class StockCacheService:

    @staticmethod
    def get_stock(store_id, item_id):
        key = f"stock:{store_id}:{item_id}"
        data = cache.get(key)

        if data:
            return json.loads(data)

        # If not cached, fetch from DB
        try:
            stock = StockItem.objects.get(store_id=store_id, item_id=item_id)
            data = {
                "store_id": store_id,
                "item_id": item_id,
                "quantity": stock.quantity
            }
            cache.set(key, json.dumps(data), timeout=3600)
            return data
        except StockItem.DoesNotExist:
            return {"store_id": store_id, "item_id": item_id, "quantity": 0}

    @staticmethod
    def invalidate_stock(store_id, item_id):
        key = f"stock:{store_id}:{item_id}"
        cache.delete(key)
