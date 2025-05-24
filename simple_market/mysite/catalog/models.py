from datetime import date
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price =models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def get_discounted_price(self):
        return self.price

    def __str__(self):
        return f"{self.name} - {self.price} грн"


class DiscountedProduct(Product):
    discounted_percent = models.PositiveIntegerField(default=10)

    def get_discounted_price(self):
        return self.price * (1 - self.discounted_percent/100)

class SundayProduct(Product):
    file_url = models.URLField()

    def get_discounted_price(self):
        today = date.today()
        if today.weekday() == 6:
            return self.price * 0.90
        return self.price

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.get_discounted_price() * self.quantity

class Cart(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"
