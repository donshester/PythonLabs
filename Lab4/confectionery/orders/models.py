from django.db import models
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    sale_date = models.DateField()
    delivery_date = models.DateField()

    def __str__(self):
        return f"Order #{self.pk} - Customer: {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"Order #{self.order.pk} - Product: {self.product.name} - Quantity: {self.quantity}"
