import django_filters
from .models import Item


class ItemFilter(django_filters.FilterSet):
    stock_status = django_filters.ChoiceFilter(choices=Item.StockStatus.choices)
    SKU = django_filters.CharFilter(lookup_expr="iexact")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Item
        fields = ["stock_status", "SKU", "name"]
