from django.db import models
from django.contrib.auth.models import User, AnonymousUser

from products.models import Product, UserPurchase

class UserProfile(models.Model):
    # This Line is required. Links UserProfile to a User Model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    paypal = models.EmailField(max_length=70, null=True, blank=False, unique=True)
    phonenumber = models.CharField(max_length=40, null=True, blank=False, unique=True)

    #Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
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
        if product in purchase.product_set.all():
            return True
    return False
User.has_purchased = has_purchased

def purchased_products(self):
    return [product for purchase in UserPurchase.objects.filter(user=self) for product in purchase.product_set.all()]
User.purchased_products = purchased_products

def flatten(alist):
    return [item for sublist in alist for item in sublist]

def sell_transactions(self):
    # TODO Optimize this to narrow down records at the DB level.
    # Ideally Product <-> UserPurchase should not be many-to-many, but
    # one-to-many, as each Product is unique and can be in just a single
    # UserPurchase.
    products = Product.objects.filter(user=self)
    return flatten(list(UserPurchase.objects.filter(product=product)) for product in products)
User.sell_transactions = sell_transactions

def can_review(self, other_user):
    sellers = [product.user for product in self.purchased_products()]
    buyers = [purchase.user for purchase in self.sell_transactions()]
    return self != other_user and ((other_user in sellers) or (other_user in buyers))
User.can_review = can_review
AnonymousUser.can_review = lambda s,u: False
