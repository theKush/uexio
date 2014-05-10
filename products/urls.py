from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('products.views',
    url(r'^$', 'list_all', name="all_products"),
    url(r'^search/', 'search_products', name="search_products"),
    url(r'^category/(?P<slug>.*)', 'category', name="category"),
    url(r'^add/', 'add_product', name="add_product"),
    url(r'^(?P<id>.*)/comment/', 'comment', name="comment"),
    url(r'^(?P<id>.*)/activate/', 'activate_product', name="activate_product"),
    url(r'^(?P<id>.*)/deactivate/', 'deactivate_product', name="deactivate_product"),
    url(r'^(?P<id>.*)/coupons/', 'manage_coupons', name="manage_coupons"),
    url(r'^(?P<id>.*)/images/', 'manage_product_image', name="manage_product_image"),
    url(r'^(?P<id>.*)/edit/', 'edit_product', name="edit_product"),
    url(r'^(?P<id>.*)/mark_as_received/', 'mark_as_received', name="mark_as_received"),
    url(r'^(?P<id>[0-9]+)/(?P<slug>.*)/$', 'single', name="single_product"),
)
