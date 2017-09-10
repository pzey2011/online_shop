from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Item, Group, Order
from django.contrib.auth.models import User
from .serializers import ItemSerializer, UserSerializer, OrderSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrAdmin


class ItemViewSet(
    viewsets.ModelViewSet):  # Quering Item from Database and Set which Serializer Shows this ViewSet and responses to Api
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class GroupItemViewSet(
    viewsets.ModelViewSet):  # Quering Items from Special Group from Database and Set which Serializer Shows this ViewSet and responses to Api
    serializer_class = ItemSerializer

    def get_queryset(self):  # Filter Items object with Special Group Id with pk parameter from Url
        PK = self.kwargs['pk']
        return get_object_or_404(Group, pk=PK).item_set.all()


class UserViewSet(
    viewsets.ReadOnlyModelViewSet):  # Quering User form Database and Set which Serializer Shows this ViewSet and responses to Api
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUserViewSet(CreateAPIView):
    permission_classes = {AllowAny,}
    serializer_class = UserSerializer




class GroupViewSet(
    viewsets.ModelViewSet):  # Quering Group form Database and Set which Serializer Shows this ViewSet and responses to Api
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OrderViewSet(
    viewsets.ModelViewSet):  # Quering Order form Database and Set which Serializer Shows this ViewSet and responses to Api

    serializer_class = OrderSerializer
    permission_classes = {IsAuthenticated, IsOwnerOrAdmin, }

    def perform_create(self, serializer):  # initializing the owner of the order
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            Orders = []
            for order in Order.objects.all():
                if order.owner == self.request.user:
                    Orders.append(order)
            return Orders