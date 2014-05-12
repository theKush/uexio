from django.db import models
from django.contrib.auth.models import User

from products.models import Product

# model that creates the shopping cart
class Shoppingcart(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # calculate the total price before discount
    def total_price(self):
        return sum(item.product.price for item in self.shoppingcartitem_set.all())
    # calculate the total discout
    def total_discount(self):
        return sum(item.discount or 0 for item in self.shoppingcartitem_set.all())
    # calculate the total price of the cart after the discount
    def total_after_discount(self):
        return self.total_price() - self.total_discount()
    # create a transaction name with cart id for usage in PayPal
    def transaction_name(self):
        return 'Uexio transaction #%s' % self.id

    def __unicode__(self):
        return str(self.id)
# model for a shoping cart item thats in the cart
class ShoppingcartItem(models.Model):
    shoppingcart = models.ForeignKey(Shoppingcart)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return "%s" %(self.product.title)
