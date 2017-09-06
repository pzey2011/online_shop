from django.contrib import admin
from .models import Item, Group, Order

admin.site.register(Group)
admin.site.register(Item)
admin.site.register(Order)
