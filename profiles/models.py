from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class UserPurchase(models.Model):
    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product)

    def __unicode__(self, ):
        return self.user.username

def has_purchased(self, product):
    for purchase in UserPurchase.objects.filter(user=self):
        if product in purchase.products.all():
            return True
    return False
User.has_purchased = has_purchased

def purchased_products(self):
    return [product for purchase in UserPurchase.objects.filter(user=self) for product in purchase.products.all()]
User.purchased_products = purchased_products
