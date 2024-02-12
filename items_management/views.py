from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from inventory_dashboard.settings import StandardResultsSetPagination

from .filters import ItemFilter
from .models import Item
from .serializers import ItemSerializer


parameter_description = [
    openapi.Parameter(
        name="ordering",
        in_=openapi.IN_QUERY,
        description=(
            "Which field to use when ordering the results. "
            "Add '-' before the field name for descending order. "
            "e.g., 'name' for ascending or '-name' for descending."
        ),
        type=openapi.TYPE_STRING,
        enum=[
            "SKU",
            "-SKU",
            "name",
            "-name",
            "category__name",
            "-category__name",
            "stock_status",
            "-stock_status",
            "in_stock",
            "-in_stock",
            "available_stock",
            "-available_stock",
        ],
    ),
]


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing items.

    Provides CRUD operations for items and supports filtering, ordering, and pagination.

    Attributes:
        serializer_class (class): The serializer class for items.
        filter_backends (list): The filter backends to use for filtering items.
        filterset_class (class): The filterset class for items.
        ordering_fields (list): The fields that can be used for ordering items.
        pagination_class (class): The pagination class for items.
        permission_classes (list): The permission classes required for accessing items.
        lookup_field (str): The lookup field for retrieving items.
    """

    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering_fields = [
        "SKU",
        "name",
        "category__name",
        "stock_status",
        "in_stock",
        "available_stock",
    ]
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "SKU"  # Use SKU as the lookup field instead of id

    def get_object(self):
        """
        Retrieve a specific item by SKU.

        Returns:
            Item: The item object.
        """
        sku = self.kwargs.get("SKU")
        return get_object_or_404(Item, SKU=sku)

    def get_queryset(self):
        """
        Get the queryset for items.

        Returns:
            QuerySet: The queryset for items.
        """
        return Item.objects.order_by("SKU")

    @swagger_auto_schema(manual_parameters=parameter_description)
    def list(self, request, *args, **kwargs):
        """
        List all items.

        Returns:
            Response: The response containing the list of items.
        """
        cache_key = f"item_list_{request.get_full_path()}"
        cache_data = cache.get(cache_key)

        if not cache_data:
            response = super(ItemViewSet, self).list(request, *args, **kwargs)
            cache_data = response.data
            cache.set(cache_key, cache_data, timeout=60 * 15)
            return response
        return Response(cache_data)

    def perform_create(self, serializer):
        """
        Perform additional actions after creating an item.

        Args:
            serializer (Serializer): The serializer instance.
        """
        super().perform_create(serializer)
        self.clear_list_cache()

    def perform_update(self, serializer):
        """
        Perform additional actions after updating an item.

        Args:
            serializer (Serializer): The serializer instance.
        """
        super().perform_update(serializer)
        self.clear_list_cache()

    def perform_destroy(self, instance):
        """
        Perform additional actions after deleting an item.

        Args:
            instance (Item): The item instance.
        """
        super().perform_destroy(instance)
        self.clear_list_cache()

    def clear_list_cache(self):
        """
        Invalidate cache for the list view.
        """
        # Here you might want to be more specific or use a pattern to match cache keys
        cache.delete_pattern("item_list_*")
