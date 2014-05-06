from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Shoppingcart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def total_price(self):
        return sum(item.product.price for item in self.shoppingcartitem_set.all())

    def total_discount(self):
        return sum(item.discount or 0 for item in self.shoppingcartitem_set.all())

    def total_after_discount(self):
        return self.total_price() - self.total_discount()

    def __unicode__(self):
        return str(self.id)

class ShoppingcartItem(models.Model):
    shoppingcart = models.ForeignKey(Shoppingcart)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return "%s" %(self.product.title)
