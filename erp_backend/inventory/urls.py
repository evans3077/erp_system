# inventory/urls.py
from django.urls import path
from .views import (
    StoreListView,
    ItemListView,
    CreateStockRequestView,
    ApproveRequestView,
    IssueRequestView,
    receive_stock_view,
    return_stock_view,
    StockMovementListView,
    check_stock_view, 
    issue_stock_view
)

urlpatterns = [
    path("stores/", StoreListView.as_view()),
    path("items/", ItemListView.as_view()),

    # Stock Request Workflow
    path("request/", CreateStockRequestView.as_view()),
    path("request/<int:pk>/approve/", ApproveRequestView.as_view()),
    path("request/<int:pk>/issue/", IssueRequestView.as_view()),

    # Stock Receipt & Return
    path("stock/receive/", receive_stock_view),
    path("stock/return/", return_stock_view),

    # Stock Movements
    path("stock/movements/", StockMovementListView.as_view()),

    # Check Stock Quantity
    path("stock/check/", check_stock_view),


    path("issue_stock/", issue_stock_view),

]

