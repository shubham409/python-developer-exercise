from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Node,
    Edge,
    RouteHistory
)


class NodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "id",
    )


class EdgeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "destination",
        "latency",
    )

    search_fields = (
        "source__name",
        "destination__name",
    )

    list_filter = (
        "source",
        "destination",
    )

    ordering = (
        "id",
    )

    autocomplete_fields = (
        "source",
        "destination",
    )


class RouteHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "destination",
        "total_latency",
        "created_at",
    )

    search_fields = (
        "source__name",
        "destination__name",
    )

    list_filter = (
        "source",
        "destination",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    autocomplete_fields = (
        "source",
        "destination",
    )


admin.site.register(
    Node,
    NodeAdmin
)

admin.site.register(
    Edge,
    EdgeAdmin
)

admin.site.register(
    RouteHistory,
    RouteHistoryAdmin
)