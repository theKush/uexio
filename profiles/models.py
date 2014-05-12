from django.db import models
from django.contrib.auth.models import User, AnonymousUser

from products.models import Product, UserPurchase
# create a model with addition requirements of paypal and phonenumber
class UserProfile(models.Model):
    # This Line is required. Links UserProfile to a User Model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    paypal = models.EmailField(max_length=70, null=True, blank=False, unique=True)
    phonenumber = models.CharField(max_length=40, null=True, blank=False, unique=True)

    #Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
# create a model for seller review(feedback) and allowing user ratings
class SellerReview(models.Model):
    RATING_CHOICES = ((1,'*'), (2,'**'), (3,'***'), (4,'****'), (5,'*****'))
    seller = models.ForeignKey(User, null=False, blank=False, related_name='reviews_received')
    author = models.ForeignKey(User, null=False, blank=False, related_name='reviews_made')
    content = models.CharField(max_length=500)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.content)
# check if user has purchased a product
def has_purchased(self, product):
    for purchase in UserPurchase.objects.filter(user=self):
        if product in purchase.product_set.all():
            return True
    return False
User.has_purchased = has_purchased
# get a list of purchased products
def purchased_products(self):
    return [product for purchase in UserPurchase.objects.filter(user=self) for product in purchase.product_set.all()]
User.purchased_products = purchased_products

def flatten(alist):
    return [item for sublist in alist for item in sublist]
# get the transactions of user purchases
def sell_transactions(self):
    return UserPurchase.objects.filter(product__user=self).all()
User.sell_transactions = sell_transactions
# check to see if a user can review other user. A buyer can only review an user if there is a transaction between them, and vice versa.
def can_review(self, other_user):
    sellers = [product.user for product in self.purchased_products()]
    buyers = [purchase.user for purchase in self.sell_transactions()]
    return self != other_user and ((other_user in sellers) or (other_user in buyers))
User.can_review = can_review
AnonymousUser.can_review = lambda s,u: False
# average the user ratings
def avg(seq):
    if len(seq) == 0:
        return None
    return sum(seq) / float(len(seq))
# display the averaged user ratings.
def avg_rating(self):
    return avg(self.reviews_received.values_list('rating', flat=True).all())
User.avg_rating = avg_rating
