# inventory/views.py
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.stock_service import StockService
from rest_framework.decorators import api_view
from inventory.models import Store, Item
from .models import Store, Item, StockRequest
from .serializers import (
    StoreSerializer, ItemSerializer,
    StockRequestSerializer
)



class StoreListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ItemListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


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
        try:
            movement = StockService.issue_stock(request_obj, issued_by=request.user)
            return Response({
                "status": "issued",
                "movement_id": movement.id,
                "stock_remaining": movement.store_item.quantity
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def receive_stock_view(request):
    """
    Manager receives items added by storekeeper.
    Expects: store_id, item_id, quantity
    """
    store_id = request.data.get("store_id")
    item_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    store = Store.objects.get(id=store_id)
    item = Item.objects.get(id=item_id)

    stock_item = StockService.receive_stock(
        store=store,
        item=item,
        quantity=quantity,
        created_by=request.user,
        approved_by=request.user  # assuming manager is the request user
    )

    return Response({
        "message": "Stock received successfully",
        "store_item": {
            "store": store.name,
            "item": item.name,
            "quantity": stock_item.quantity
        }
    })