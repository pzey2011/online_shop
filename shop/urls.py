from django.conf.urls import url
from .views import OrderViewSet, UserViewSet , ItemViewSet ,GroupItemViewSet, GroupViewSet, CreateUserViewSet,SearchItemViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

search_item_list= SearchItemViewSet.as_view({
    'get': 'list',
})

item_list = ItemViewSet.as_view({
    'get': 'list',
})
group_list = GroupViewSet.as_view({
    'get': 'list',
})
group_item_list=GroupItemViewSet.as_view({
    'get': 'list',
})
order_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
order_detail = OrderViewSet.as_view({
    'get': 'retrieve',
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    url(r'^orders/$', order_list, name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', order_detail, name='order-detail'),
    url(r'^items/$', item_list, name='item-list'),
    url(r'^items/search/$', search_item_list, name='search-item-list'),
    url(r'^groups/$', group_list, name='group-list'),
    url(r'^groups/(?P<pk>[0-9]+)/items/$', group_item_list, name='group-item-list'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^register/$', CreateUserViewSet.as_view(), name='register'),

])