from django.db import models

# Create your models here.


class Node(models.Model):
    '''
    Model to store node of the network.
    '''
    
    # name of the node ( unique as given in the problem )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Edge(models.Model):
    '''
    Model to connect from one node to another and store
    relevant info e.g. latency of the edge.
    '''
    
    # source node of the edge
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="outgoing_edges"
    )
    destination = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="incoming_edges"
    )
    latency = models.FloatField()

    class Meta:
        unique_together = ("source", "destination")

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class RouteHistory(models.Model):
    '''
    Model to store route history details
    '''
    
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="route_source_history"
    )
    destination = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="route_destination_history"
    )

    total_latency = models.FloatField()

    path = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} -> {self.destination}"