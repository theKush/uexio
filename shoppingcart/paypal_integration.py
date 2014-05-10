from itertools import chain
from urllib2 import urlopen

import django_rq

from django.db import transaction

from uexio.settings import PAYPAL_EMAIL, PAYPAL_HOST

from products.models import UserPurchase
from .models import Shoppingcart

IPN_URLSTRING = 'https://%s/cgi-bin/webscr' % PAYPAL_HOST
IPN_VERIFY_EXTRA_PARAMS = [('cmd', '_notify-validate')]


def transaction_data_matches(cart, params):
    return params['payment_status'] == 'Completed' and \
        params['receiver_email'] == PAYPAL_EMAIL and \
        float(params['mc_gross']) == cart.total_after_discount() and \
        params['mc_currency'] == 'USD' and \
        params['item_name'] == cart.transaction_name()

def is_paypal_notification_valid(params):
    verify_args = chain(params.iteritems(), IPN_VERIFY_EXTRA_PARAMS)
    verify_string = '&'.join(('%s=%s' % (param, value) for param, value in verify_args))
    response = urlopen(IPN_URLSTRING, data=verify_string)
    status = response.read()
    return status == 'VERIFIED'

def queue_paypal_notification(cart, params):
    django_rq.enqueue(process_paypal_notification, cart.id, dict([k, v[0]] for k, v in dict(params).iteritems()))

@transaction.atomic
def process_paypal_notification(cart_id, params):
    cart = Shoppingcart.objects.get(id=cart_id)
    if is_paypal_notification_valid(params):
        purchase = UserPurchase(user=cart.user,
                                transaction_id=cart.id,
                                total=cart.total_after_discount())
        purchase.save()
        for item in cart.shoppingcartitem_set.all():
            product = item.product
            product.purchase = purchase
            product.status = Product.PURCHASED
            product.sold_for = product.price - (item.discount or 0)
            product.save()
        cart.delete()
    else:
        raise RuntimeError("Paypal IPN verification failed")
