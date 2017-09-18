from django.contrib import admin
from .models import Item, Group, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'total_price', 'time')
    readonly_fields = ('items', 'total_price', 'owner')
    search_fields = ['owner__username', 'items__title']
    list_filter = ('status' ,)
    list_display_links = ('owner','total_price' , 'time')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title','price', 'stock', 'image')
    search_fields = ['title']
    list_filter = ('group__title' ,)


admin.site.register(Group)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
