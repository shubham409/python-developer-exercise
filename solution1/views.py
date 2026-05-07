from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Node, Edge, RouteHistory
from .serializers import NodeSerializer, EdgeSerializer
from .algorithms import shortest_path
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

class AddNodeAPIView(APIView):

    def post(self, request):
        serializer = NodeSerializer(data=request.data)

        if serializer.is_valid():
            node = serializer.save()

            return Response(
                NodeSerializer(node).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AddEdgeAPIView(APIView):

    def post(self, request):
        serializer = EdgeSerializer(data=request.data)

        if serializer.is_valid():
            edge = serializer.save()

            return Response(
                {
                    "id": edge.id,
                    "source": edge.source.name,
                    "destination": edge.destination.name,
                    "latency": edge.latency
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ShortestRouteAPIView(APIView):

    def post(self, request):
        source = request.data.get("source")
        destination = request.data.get("destination")

        if not source or not destination:
            return Response(
                {
                    "error": "Source and destination are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            source_node = Node.objects.get(name=source)
            destination_node = Node.objects.get(name=destination)
        except Node.DoesNotExist:
            return Response(
                {
                    "error": "Invalid source or destination node"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = shortest_path(
            source_node,
            destination_node
        )

        if not result:
            return Response(
                {
                    "error": (
                        f"No path exists between "
                        f"{source} and {destination}"
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        RouteHistory.objects.create(
            source=source_node,
            destination=destination_node,
            total_latency=result["total_latency"],
            path=result["path"]
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )


class RouteHistoryAPIView(APIView):

    def get(self, request):
        queryset = RouteHistory.objects.select_related(
            "source",
            "destination"
        ).all().order_by("-created_at")

        source = request.GET.get("source")
        destination = request.GET.get("destination")
        limit = request.GET.get("limit")
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")

        if source:
            queryset = queryset.filter(source__name=source)

        if destination:
            queryset = queryset.filter(
                destination__name=destination
            )

        if date_from:
            date_from = parse_datetime(date_from)
            queryset = queryset.filter(created_at__date__gte=date_from)

        if date_to:
            date_to = parse_datetime(date_to)
            queryset = queryset.filter(created_at__date__lte=date_to)

        if limit:
            queryset = queryset[:int(limit)]

        response = []

        for route in queryset:
            response.append({
                "id": route.id,
                "source": route.source.name,
                "destination": route.destination.name,
                "total_latency": route.total_latency,
                "path": route.path,
                "created_at": route.created_at
            })

        return Response(
            response,
            status=status.HTTP_200_OK
        )
        
class NodeListAPIView(APIView):

    def get(self, request):
        nodes = Node.objects.all().order_by("id")

        serializer = NodeSerializer(
            nodes,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class EdgeListAPIView(APIView):

    def get(self, request):
        edges = Edge.objects.select_related(
            "source",
            "destination"
        ).all().order_by("id")

        response = []

        for edge in edges:
            response.append({
                "id": edge.id,
                "source": edge.source.name,
                "destination": edge.destination.name,
                "latency": edge.latency
            })

        return Response(
            response,
            status=status.HTTP_200_OK
        )

class DeleteNodeAPIView(APIView):

    def delete(self, request, node_id):
        node = get_object_or_404(
            Node,
            id=node_id
        )

        node.delete()

        return Response(
            {
                "message": "Node deleted successfully"
            },
            status=status.HTTP_200_OK
        )
        
class DeleteEdgeAPIView(APIView):

    def delete(self, request, edge_id):
        edge = get_object_or_404(
            Edge,
            id=edge_id
        )

        edge.delete()

        return Response(
            {
                "message": "Edge deleted successfully"
            },
            status=status.HTTP_200_OK
        )