from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shoppingcart.views',
    url(r'^$', 'shoppingcart', name='shoppingcart'),
    url(r'^update_cart/(?P<id>.*)', 'update_cart', name="update_cart"),
    url(r'^apply_coupon', 'apply_coupon', name="apply_coupon"),
)
