from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    Node,
    Edge,
    RouteHistory
)


class NetworkAPITestCase(APITestCase):

    def setUp(self):

        self.server_a = Node.objects.create(
            name="ServerA"
        )

        self.server_b = Node.objects.create(
            name="ServerB"
        )

        self.server_c = Node.objects.create(
            name="ServerC"
        )

        self.edge_ab = Edge.objects.create(
            source=self.server_a,
            destination=self.server_b,
            latency=10
        )

        self.edge_bc = Edge.objects.create(
            source=self.server_b,
            destination=self.server_c,
            latency=5
        )

    # =========================================================
    # NODE APIs
    # =========================================================

    def test_add_node_success(self):

        response = self.client.post(
            "/solution1/nodes",
            {
                "name": "ServerD"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["name"],
            "ServerD"
        )

    def test_add_node_duplicate(self):

        response = self.client.post(
            "/solution1/nodes",
            {
                "name": "ServerA"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_list_nodes(self):

        response = self.client.get(
            "/solution1/nodes/list"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            3
        )

    def test_delete_node_success(self):

        response = self.client.delete(
            f"/solution1/nodes/{self.server_a.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            Node.objects.filter(
                id=self.server_a.id
            ).exists()
        )

    def test_delete_node_not_found(self):

        response = self.client.delete(
            "/solution1/nodes/999"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    # =========================================================
    # EDGE APIs
    # =========================================================

    def test_add_edge_success(self):

        server_d = Node.objects.create(
            name="ServerD"
        )

        response = self.client.post(
            "/solution1/edges",
            {
                "source": "ServerA",
                "destination": "ServerD",
                "latency": 7
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["latency"],
            7
        )

    def test_add_edge_invalid_latency(self):

        response = self.client.post(
            "/solution1/edges",
            {
                "source": "ServerA",
                "destination": "ServerB",
                "latency": -5
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_add_edge_duplicate(self):

        response = self.client.post(
            "/solution1/edges",
            {
                "source": "ServerA",
                "destination": "ServerB",
                "latency": 10
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_add_edge_node_not_found(self):

        response = self.client.post(
            "/solution1/edges",
            {
                "source": "ServerA",
                "destination": "UnknownServer",
                "latency": 10
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_list_edges(self):

        response = self.client.get(
            "/solution1/edges/list"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )

    def test_delete_edge_success(self):

        response = self.client.delete(
            f"/solution1/edges/{self.edge_ab.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            Edge.objects.filter(
                id=self.edge_ab.id
            ).exists()
        )

    def test_delete_edge_not_found(self):

        response = self.client.delete(
            "/solution1/edges/999"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    # =========================================================
    # SHORTEST ROUTE APIs
    # =========================================================

    def test_shortest_route_success(self):

        response = self.client.post(
            "/solution1/routes/shortest",
            {
                "source": "ServerA",
                "destination": "ServerC"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["total_latency"],
            15
        )

        self.assertEqual(
            response.data["path"],
            [
                "ServerA",
                "ServerB",
                "ServerC"
            ]
        )

    def test_shortest_route_invalid_node(self):

        response = self.client.post(
            "/solution1/routes/shortest",
            {
                "source": "ServerA",
                "destination": "Unknown"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_shortest_route_no_path(self):

        isolated_node = Node.objects.create(
            name="ServerD"
        )

        response = self.client.post(
            "/solution1/routes/shortest",
            {
                "source": "ServerA",
                "destination": "ServerD"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    # =========================================================
    # ROUTE HISTORY APIs
    # =========================================================

    def test_route_history_success(self):

        RouteHistory.objects.create(
            source=self.server_a,
            destination=self.server_c,
            total_latency=15,
            path=[
                "ServerA",
                "ServerB",
                "ServerC"
            ]
        )

        response = self.client.get(
            "/solution1/routes/history"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

    def test_route_history_filter_by_source(self):

        RouteHistory.objects.create(
            source=self.server_a,
            destination=self.server_c,
            total_latency=15,
            path=[
                "ServerA",
                "ServerB",
                "ServerC"
            ]
        )

        response = self.client.get(
            "/solution1/routes/history?source=ServerA"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

    def test_route_history_filter_by_destination(self):

        RouteHistory.objects.create(
            source=self.server_a,
            destination=self.server_c,
            total_latency=15,
            path=[
                "ServerA",
                "ServerB",
                "ServerC"
            ]
        )

        response = self.client.get(
            "/solution1/routes/history?destination=ServerC"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

    def test_route_history_limit(self):

        RouteHistory.objects.create(
            source=self.server_a,
            destination=self.server_b,
            total_latency=10,
            path=[
                "ServerA",
                "ServerB"
            ]
        )

        RouteHistory.objects.create(
            source=self.server_b,
            destination=self.server_c,
            total_latency=5,
            path=[
                "ServerB",
                "ServerC"
            ]
        )

        response = self.client.get(
            "/solution1/routes/history?limit=1"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )