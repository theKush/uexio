from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('products.views',
    url(r'^$', 'list_all', name="all_products"),
    url(r'^(?P<slug>.*)/$', 'single', name="single_product"),
)
