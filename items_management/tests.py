from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Category, Item, Tag


class ItemViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Art Supplies")
        self.tag = Tag.objects.create(name="Portable")
        self.item = Item.objects.create(
            SKU="TEST123",
            name="Test Item",
            category=self.category,
            stock_status=Item.StockStatus.IN_STOCK,
            in_stock=10,
            available_stock=5,
        )
        self.item.tags.add(self.tag)

        cache.clear()

    def tearDown(self):
        cache.clear()

        self.item.delete()
        self.tag.delete()
        self.category.delete()
        self.user.delete()

    def test_create_item(self):
        url = reverse("items-list")
        data = {
            "SKU": "NEW123",
            "name": "New Item",
            "category": self.category.id,
            "stock_status": "IN",
            "in_stock": 20,
            "available_stock": 10,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 32)

    def test_update_item_put(self):
        url = reverse("items-detail", kwargs={"SKU": self.item.SKU})
        data = {
            "SKU": self.item.SKU,
            "name": "Updated Item",
            "category": self.category.id,
            "stock_status": "OUT",
            "in_stock": 0,
            "available_stock": 0,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")

    def test_update_item_patch(self):
        url = reverse("items-detail", kwargs={"SKU": self.item.SKU})
        data = {"name": "Partially Updated Item"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Partially Updated Item")

    def test_delete_item(self):
        url = reverse("items-detail", kwargs={"SKU": self.item.SKU})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Item.DoesNotExist):
            self.item.refresh_from_db()

    def test_list_items(self):
        url = reverse("items-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)

    def test_retrieve_item(self):
        url = reverse("items-detail", kwargs={"SKU": self.item.SKU})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["SKU"], self.item.SKU)

    def test_ordering_items(self):
        url = reverse("items-list") + "?ordering=category__name"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["category"]["name"], self.item.category.name
        )

    def test_10_records_per_page(self):
        url = reverse("items-list")
        response = self.client.get(url)
        self.assertTrue("count" in response.data)
        self.assertLessEqual(len(response.data["results"]), 10)

    def test_filtering_items_by_status(self):
        url = reverse("items-list") + "?stock_status=IN"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["stock_status"], "IN")

    def test_list_cache_invalidation_on_create(self):
        list_url = reverse("items-list")

        self.client.get(list_url)
        self.assertIsNotNone(cache.get(f"item_list_{list_url}"))

        data = {
            "SKU": "NEW123",
            "name": "New Item",
            "category": self.category.id,
            "stock_status": "IN",
            "in_stock": 20,
            "available_stock": 10,
        }
        self.client.post(list_url, data, format="json")

        self.assertIsNone(cache.get(f"item_list_{list_url}"))

    def test_list_cache_invalidation_on_update(self):
        list_url = reverse("items-list")
        detail_url = reverse("items-detail", kwargs={"SKU": self.item.SKU})

        self.client.get(list_url)
        self.assertIsNotNone(cache.get(f"item_list_{list_url}"))

        update_data = {
            "SKU": "UPDATE123",
            "name": "New Item",
            "category": self.category.id,
            "stock_status": "IN",
            "in_stock": 20,
            "available_stock": 10,
        }
        self.client.put(detail_url, update_data, format="json")

        self.assertIsNone(cache.get(f"item_list_{list_url}"))

    def test_list_cache_invalidation_on_delete(self):
        list_url = reverse("items-list")
        detail_url = reverse("items-detail", kwargs={"SKU": self.item.SKU})

        self.client.get(list_url)
        self.assertIsNotNone(cache.get(f"item_list_{list_url}"))

        self.client.delete(detail_url)

        self.assertIsNone(cache.get(f"item_list_{list_url}"))
