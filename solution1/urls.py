from django.urls import path

from .views import (
    AddNodeAPIView,
    AddEdgeAPIView,
    ShortestRouteAPIView,
    RouteHistoryAPIView,
    NodeListAPIView,
    EdgeListAPIView,
    DeleteEdgeAPIView,
    DeleteNodeAPIView,
)

urlpatterns = [
    
    # Create
    path("nodes",AddNodeAPIView.as_view()),
    path("edges",AddEdgeAPIView.as_view()),
    
    # Routes
    path("routes/shortest",ShortestRouteAPIView.as_view()),
    path("routes/history",RouteHistoryAPIView.as_view()),

    # List
    path("nodes/list", NodeListAPIView.as_view()),
    path("edges/list", EdgeListAPIView.as_view()),

    # Delete
    path("nodes/<int:node_id>", DeleteNodeAPIView.as_view()),
    path("edges/<int:edge_id>", DeleteEdgeAPIView.as_view()),
]