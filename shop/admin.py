from django.contrib import admin
from .models import Item, Group, Order

class OrderAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('items', 'total_price','owner')
        return self.readonly_fields
admin.site.register(Group)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
