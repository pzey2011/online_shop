from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Item, Group, Order
from django.contrib.auth.models import User
from .serializers import ItemSerializer, UserSerializer, OrderSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404


class ItemViewSet(
    viewsets.ModelViewSet):  # Quering Item from Database and Set which Serializer Shows this ViewSet and responses to Api
    queryset = Item.objects.all()
    print('khar')
    serializer_class = ItemSerializer

class SearchItemViewSet(viewsets.ModelViewSet):

    serializer_class = ItemSerializer

    def get_queryset(self):  # Filter Items object with Special Group Id with pk parameter from Url
        PK = self.request.query_params.get('q', None)
        print(PK)
        items= Item.objects.filter(title__contains=PK)
        return items

class GroupItemViewSet(
    viewsets.ModelViewSet):  # Quering Items from Special Group from Database and Set which Serializer Shows this ViewSet and responses to Api
    serializer_class = ItemSerializer

    def get_queryset(self):  # Filter Items object with Special Group Id with pk parameter from Url
        PK = self.kwargs['pk']
        return get_object_or_404(Group, pk=PK).item_set.all()


class UserViewSet(
    viewsets.ReadOnlyModelViewSet):  # Quering User form Database and Set which Serializer Shows this ViewSet and responses to Api
    serializer_class = UserSerializer
    permission_classes = {IsAuthenticated, }

    def get_queryset(self):  # custom query_set function
        if self.request.user.is_superuser:  # if the user is admin it returns all Orders
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.id)


class CreateUserViewSet(CreateAPIView):
    permission_classes = {AllowAny, }
    serializer_class = UserSerializer


class GroupViewSet(
    viewsets.ModelViewSet):  # Quering Group form Database and Set which Serializer Shows this ViewSet and responses to Api
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class OrderViewSet(
    viewsets.ModelViewSet):  # Quering Order form Database and Set which Serializer Shows this ViewSet and responses to Api

    serializer_class = OrderSerializer
    permission_classes = {IsAuthenticated, }

    def perform_create(self, serializer):  # initializing the owner of the order
        serializer.save(owner=self.request.user)

    def get_queryset(self):  # custom query_set function
        if self.request.user.is_superuser:  # if the user is admin it returns all Orders
            return Order.objects.all()
        else:
            return self.request.user.orders
