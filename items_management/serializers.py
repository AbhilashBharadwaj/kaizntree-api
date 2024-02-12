
from rest_framework import serializers
from .models import Item, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ['SKU', 'name', 'category', 'tags',
                  'stock_status', 'in_stock', 'available_stock']
