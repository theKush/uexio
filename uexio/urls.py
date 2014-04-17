from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # regular expression below sets up the path for the app, more info in settings
    url(r'^$', 'products.views.list_all', name="all_products"),
    url(r'^lib/', 'profiles.views.library', name="library"),
    url(r'^products/', include('products.urls')),
    url(r'^shoppingcart/', include('shoppingcart.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # The line below enables admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
