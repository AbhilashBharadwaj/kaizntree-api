from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Represents a cateogry for an item in the inventory.
    """

    name = models.CharField(max_length=100, unique=True)
    # Additional fields if necessary

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag for an item in the inventory.
    """

    name = models.CharField(max_length=100, unique=True)
    # Additional fields if necessary

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Represents an item in the inventory.

    Attributes:
    - SKU: The stock keeping unit of the item.
    - name: The name of the item.
    - category: The category to which the item belongs.
    - tags: The tags associated with the item.
    - stock_status: The current stock status of the item.
    - in_stock: The quantity of the item currently in stock.
    - available_stock: The quantity of the item available for sale.
    """

    class StockStatus(models.TextChoices):
        """
        Represents the stock status of an item.

        Possible values:
        - IN_STOCK: Item is currently in stock.
        - OUT_OF_STOCK: Item is currently out of stock.
        - BACKORDER: Item is on backorder.
        """

        IN_STOCK = "IN", _("In Stock")
        OUT_OF_STOCK = "OUT", _("Out of Stock")
        BACKORDER = "BO", _("Backorder")

    SKU = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    stock_status = models.CharField(
        max_length=3,
        choices=StockStatus.choices,
        default=StockStatus.IN_STOCK,
    )
    in_stock = models.DecimalField(max_digits=10, decimal_places=0)
    available_stock = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.name} ({self.SKU})"
