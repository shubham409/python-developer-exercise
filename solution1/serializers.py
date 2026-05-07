from rest_framework import serializers
from .models import Node, Edge


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "name"]


class EdgeSerializer(serializers.ModelSerializer):
    source = serializers.CharField()
    destination = serializers.CharField()

    class Meta:
        model = Edge
        fields = ["id", "source", "destination", "latency"]

    def validate(self, data):
        if data["latency"] <= 0:
            raise serializers.ValidationError(
                "Latency must be greater than 0"
            )

        try:
            source_node = Node.objects.get(name=data["source"])
            destination_node = Node.objects.get(name=data["destination"])
        except Node.DoesNotExist:
            raise serializers.ValidationError(
                "Source or destination node does not exist"
            )

        if Edge.objects.filter(
            source=source_node,
            destination=destination_node
        ).exists():
            raise serializers.ValidationError(
                "Edge already exists"
            )

        data["source_node"] = source_node
        data["destination_node"] = destination_node

        return data

    def create(self, validated_data):
        return Edge.objects.create(
            source=validated_data["source_node"],
            destination=validated_data["destination_node"],
            latency=validated_data["latency"]
        )