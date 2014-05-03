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
    url(r'^(?P<slug>.*)/comment/', 'comment', name="comment"),
    url(r'^(?P<slug>.*)/activate/', 'activate_product', name="activate_product"),
    url(r'^(?P<slug>.*)/deactivate/', 'deactivate_product', name="deactivate_product"),
    url(r'^(?P<slug>.*)/coupons/', 'manage_coupons', name="manage_coupons"),
    url(r'^(?P<slug>.*)/images/', 'manage_product_image', name="manage_product_image"),
    url(r'^(?P<slug>.*)/edit/', 'edit_product', name="edit_product"),
    url(r'^(?P<slug>.*)/$', 'single', name="single_product"),
)
