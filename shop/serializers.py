from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, Item, Group
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.validators import ValidationError

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields =('id' , 'title' , 'price' , 'comment', 'stock')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields =('id' , 'title' )


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'orders')


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.ReadOnlyField()
    total_price=serializers.ReadOnlyField()
    status=serializers.ReadOnlyField()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    class Meta:
        model = Order
        fields = ('id', 'owner',
                  'items', 'time', 'total_price', 'status')

    def validate(self, data):
        for item in data['items']:
            print(item,item.stock)
            if item.stock < 1:
                raise ValidationError('stock is not enough!')
        return data

    def create(self, validated_data):
        order = super().create(validated_data)
        order.total_price=0
        for item in order.items.all():
            order.total_price += item.price
        for item in order.items.all():
            item.stock-=1
            item.save()
        order.save()
        return order