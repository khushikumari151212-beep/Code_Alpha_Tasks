from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import MenuItem, Table, Order, Inventory
from .serializers import *

class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        total = sum(item.price for item in order.items.all())
        order.total_price = total
        order.save()


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer