from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Order, Item, Group
from rest_framework.validators import ValidationError


class ItemSerializer(serializers.ModelSerializer):  # Representation of an Item in Response of a Rest Call
    stock_status = serializers.SerializerMethodField()  # returns non-stock if the stock has no Items else returns in-stock

    class Meta:
        model = Item
        fields = ('id', 'title', 'price', 'comment', 'stock_status')

    def get_stock_status(self, obj):
        if obj.stock == 0:
            return 'non-stock'
        else:
            return 'in-stock'


class GroupSerializer(serializers.ModelSerializer):  # Representation of a Group in Response of a Rest Call

    class Meta:
        model = Item
        fields = ('id', 'title')


class UserSerializer(serializers.ModelSerializer):  # Representation of an User in Response of a Rest Call

    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email', 'orders')

    def create(self, validated_data):  # registration or user creation
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class OrderSerializer(serializers.ModelSerializer):  # Representation of a Order in Response of a Rest Call

    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ('id', 'owner',
                  'items', 'time', 'total_price', 'status')

    def validate(self, data):  # Checking remaining Items in Stock < 1 ,when costumer submit his order

        for item in data['items']:
            print(item, item.stock)
            if item.stock < 1:
                raise ValidationError('stock is not enough!')
        return data

    def create(self,
               validated_data):  # Create a new order with calculating the total price of Items and decreasing number of Items in Stock

        order = super().create(validated_data)
        order.total_price = 0
        for item in order.items.all():
            order.total_price += item.price
        for item in order.items.all():
            item.stock -= 1
            item.save()
        order.save()
        return order
