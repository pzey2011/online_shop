from django.shortcuts import render
from .models import Item, Group, Order
from django.contrib.auth.models import User
from .serializers import ItemSerializer, UserSerializer, OrderSerializer, GroupSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class GroupItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        PK = self.kwargs['pk']
        return get_object_or_404(Group, pk=PK).item_set.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
