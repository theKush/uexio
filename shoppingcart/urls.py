from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shoppingcart.views',
    url(r'^$', 'shoppingcart', name='shoppingcart'),
    url(r'^add/(?P<id>.*)', 'add_to_cart', name="add_to_cart"),
)
