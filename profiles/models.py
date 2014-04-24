from django.db import models
from django.contrib.auth.models import User

from products.models import Product

class UserProfile(models.Model):
    # This Line is required. Links UserProfile to a User Model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    paypal = models.EmailField(max_length=70, null=True, blank=False, unique=True)
    phonenumber = models.CharField(max_length=40, null=True, blank=False, unique=True)

    #Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class UserPurchase(models.Model):
    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product)

    def __unicode__(self, ):
        return self.user.username

class SellerReview(models.Model):
    seller = models.ForeignKey(User, null=False, blank=False, related_name='reviews_received')
    author = models.ForeignKey(User, null=False, blank=False, related_name='reviews_made')
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.content)

def has_purchased(self, product):
    for purchase in UserPurchase.objects.filter(user=self):
        if product in purchase.products.all():
            return True
    return False
User.has_purchased = has_purchased

def purchased_products(self):
    return [product for purchase in UserPurchase.objects.filter(user=self) for product in purchase.products.all()]
User.purchased_products = purchased_products
