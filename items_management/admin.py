from django.contrib import admin

from .models import Item
from .models import Category
from .models import Tag

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Tag)
