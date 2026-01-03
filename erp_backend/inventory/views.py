# inventory/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Store, Item, StockRequest, StockMovement
from .serializers import (
    StoreSerializer,
    ItemSerializer,
    StockRequestSerializer,
    StockMovementSerializer,
    ReturnVoucherSerializer
)
from .services.stock_service import StockService
from .services.cache_service import StockCacheService



# -------------------------
# Store & Item Views
# -------------------------
class StoreListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ItemListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# -------------------------
# Stock Request Workflow
# -------------------------
class CreateStockRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockRequestSerializer

    def perform_create(self, serializer):
        store = serializer.validated_data["store"]
        item = serializer.validated_data["item"]
        quantity = serializer.validated_data["quantity"]

        StockService.create_request(
            store=store,
            item=item,
            quantity=quantity,
            requested_by=self.request.user
        )


class ApproveRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StockRequest.objects.all()
    serializer_class = StockRequestSerializer

    def update(self, request, *args, **kwargs):
        request_obj = self.get_object()
        StockService.approve_request(request_obj, request.user)
        return Response({"status": "approved"})


class IssueRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StockRequest.objects.all()
    serializer_class = StockRequestSerializer

    def update(self, request, *args, **kwargs):
        request_obj = self.get_object()
        StockService.issue_request(request_obj, request.user)
        return Response({"status": "issued"})


# -------------------------
# Stock Receiving
# -------------------------
@api_view(["POST"])
def receive_stock_view(request):
    """
    Manager receives items added by storekeeper.
    Expects JSON: store_id, item_id, quantity
    """
    store_id = request.data.get("store_id")
    item_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    store = Store.objects.get(id=store_id)
    item = Item.objects.get(id=item_id)

    stock_movement = StockService.receive_stock(
        store=store,
        item=item,
        quantity=quantity,
        created_by=request.user,
        approved_by=request.user  # assuming manager is request user
    )

    serializer = StockMovementSerializer(stock_movement)
    return Response({
        "message": "Stock received successfully",
        "stock_movement": serializer.data
    })


# -------------------------
# Stock Return
# -------------------------
@api_view(["POST"])
def return_stock_view(request):
    """
    Return previously issued stock.
    Expects JSON: movement_id, quantity
    """
    movement_id = request.data.get("movement_id")
    quantity = request.data.get("quantity")

    movement = StockMovement.objects.get(id=movement_id)

    return_voucher = StockService.return_stock(
        movement_obj=movement,
        returned_by=request.user,
        quantity=quantity
    )

    serializer = ReturnVoucherSerializer(return_voucher)
    return Response({
        "message": "Stock returned successfully",
        "return_voucher": serializer.data
    })


class StockMovementListView(generics.ListAPIView):
    serializer_class = StockMovementSerializer

    def get_queryset(self):
        queryset = StockMovement.objects.all()
        store_id = self.request.query_params.get("store_id")
        item_id = self.request.query_params.get("item_id")

        if store_id:
            queryset = queryset.filter(store_item__store_id=store_id)
        if item_id:
            queryset = queryset.filter(store_item__item_id=item_id)

        return queryset.order_by("-timestamp")
#-----------------------
# Stock View
#-----------------------

@api_view(["GET"])
def check_stock_view(request):
    """
    Check current stock quantity.
    Expects query params: ?store_id=1&item_id=4
    """
    store_id = request.query_params.get("store_id")
    item_id = request.query_params.get("item_id")

    if not store_id or not item_id:
        return Response({"error": "store_id and item_id are required"}, status=400)

    stock = StockCacheService.get_stock(store_id, item_id)

    return Response(stock)


@api_view(["POST"])
def issue_stock_view(request):
    """
    Issue stock directly (optional if not using the request workflow)
    Expects JSON: store_id, item_id, quantity
    """
    store_id = request.data.get("store_id")
    item_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    store = Store.objects.get(id=store_id)
    item = Item.objects.get(id=item_id)

    movement = StockService.issue_stock(
        store=store,
        item=item,
        quantity=quantity,
        issued_by=request.user
    )

    serializer = StockMovementSerializer(movement)
    return Response({
        "message": "Stock issued successfully",
        "stock_movement": serializer.data
    })
