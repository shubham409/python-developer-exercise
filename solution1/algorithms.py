import heapq
from .models import Edge


def shortest_path(source_node, destination_node):
    """
    Compute the shortest path between two nodes using Dijkstra's Algorithm.

    The network is represented as a directed weighted graph where:
    - Nodes represent servers/devices.
    - Edges represent network connections.
    - Latency represents edge weight/cost.

    Why Dijkstra's Algorithm?
    -------------------------
    Dijkstra's Algorithm is used because all network latencies are
    positive values. It efficiently computes the minimum-latency
    route between source and destination nodes.

    Algorithm Workflow
    ------------------
    1. Load all edges from database.
    2. Build adjacency-list graph representation.
    3. Use a min-heap(priority queue) to always process the node
       with the currently smallest known distance.
    4. Relax neighboring edges and update shortest distances.
    5. Reconstruct final path using previous-node tracking.

    Example Graph
    -------------
    ServerA --10--> ServerB --5--> ServerC

    Internally represented as:

    {
        "ServerA": [("ServerB", 10)],
        "ServerB": [("ServerC", 5)]
    }

    Directed Graph Design
    ---------------------
    The graph is intentionally treated as directional:
        A -> B

    instead of automatically assuming:
        A <-> B

    because real-world network latency can be asymmetric due to:
    - routing differences
    - congestion
    - ISP/network path variations

    Parameters
    ----------
    source_node : Node
        Starting node for shortest-path computation.

    destination_node : Node
        Destination node for shortest-path computation.

    Returns
    -------
    dict | None

    Returns:
    {
        "total_latency": <float>,
        "path": [<node_names>]
    }

    Returns None if no path exists between nodes.

    Time Complexity
    ---------------
    O((V + E) log V)

    where:
    - V = number of nodes
    - E = number of edges

    Notes
    -----
    Current implementation rebuilds graph from database on every request.
    This is acceptable for medium-sized graphs and keeps implementation
    simple and readable.

    Possible future optimizations:
    - Redis/in-memory graph caching
    - pgRouting(PostgreSQL)
    - Graph databases like Neo4j
    - Precomputed route caching
    """

    graph = {}

    edges = Edge.objects.select_related(
        "source",
        "destination"
    ).all()

    for edge in edges:
        graph.setdefault(edge.source.name, []).append(
            (edge.destination.name, edge.latency)
        )

    distances = {
        source_node.name: 0
    }

    previous = {}

    min_heap = [
        (0, source_node.name)
    ]

    visited = set()

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == destination_node.name:
            break

        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight

            if distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(
                    min_heap,
                    (distance, neighbor)
                )

    if destination_node.name not in distances:
        return None

    path = []

    current = destination_node.name

    while current:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    return {
        "total_latency": distances[destination_node.name],
        "path": path
    }
    
