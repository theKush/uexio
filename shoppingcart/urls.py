from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shoppingcart.views',
    url(r'^$', 'shoppingcart', name='shoppingcart'),
    url(r'^add_to_cart/(?P<id>.*)', 'add_to_cart', name="add_to_cart"),
    url(r'^remove_from_cart/(?P<id>.*)', 'remove_from_cart', name="remove_from_cart"),
    url(r'^apply_coupon', 'apply_coupon', name="apply_coupon"),
    url(r'^thankyou', 'thankyou', name="thankyou"),
    url(r'^paypal_notification/(?P<id>.*)', 'paypal_notification', name="paypal_notification"),
)
