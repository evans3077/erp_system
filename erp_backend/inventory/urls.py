from django.urls import path
from .views import (
    StoreListView, ItemListView,
    CreateStockRequestView,
    ApproveRequestView, IssueRequestView, 
    receive_stock_view
)

urlpatterns = [
    path("stores/", StoreListView.as_view()),
    path("items/", ItemListView.as_view()),
    path("request/", CreateStockRequestView.as_view()),
    path("request/<int:pk>/approve/", ApproveRequestView.as_view()),
    path("request/<int:pk>/issue/", IssueRequestView.as_view()),
    path("receive/", receive_stock_view, name="receive-stock"),
    path("request/<int:pk>/issue/", IssueRequestView.as_view()),


]
