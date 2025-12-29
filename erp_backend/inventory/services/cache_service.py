from django.core.cache import cache
from stores.models import StoreItem

class StockCacheService:

    @staticmethod
    def get_stock(store_id, item_id):
        key = f"stock:{store_id}:{item_id}"
        data = cache.get(key)

        if data:
            return data
        
        try:
            store_item = StoreItem.objects.get(store_id=store_id, item_id=item_id)
            data = store_item.quantity
        except StoreItem.DoesNotExist:
            data = 0
        
        cache.set(key, data, timeout=60)  # cache 1 minute
        return data

    @staticmethod
    def invalidate_stock(store_id, item_id):
        key = f"stock:{store_id}:{item_id}"
        cache.delete(key)
