# Create your models here.
from django.db import models

# Menu Items
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Table
class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number}"


# Order
class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Completed

    def __str__(self):
        return f"Order {self.id}"


# Inventory
class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.item_name