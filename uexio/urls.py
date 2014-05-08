from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # regular expression below sets up the path for the app, more info in settings
    url(r'^$', 'pages.views.index', name="index"),
    url(r'^aboutus/', TemplateView.as_view(template_name='pages/aboutus.html')),
    url(r'^howtobuy/', TemplateView.as_view(template_name='pages/how_to_buy.html')),
    url(r'^howtosell/', TemplateView.as_view(template_name='pages/how_to_sell.html')),
    url(r'^contactus/', TemplateView.as_view(template_name='pages/contact_us.html')),
    url(r'^faq/', TemplateView.as_view(template_name='pages/faq.html')),
    url(r'^privacy/', TemplateView.as_view(template_name='pages/privacy.html')),
    url(r'^termsofuse/', TemplateView.as_view(template_name='pages/terms_of_use.html')),
    url(r'^vslocalbookstore/', TemplateView.as_view(template_name='pages/vs_local_bookstore.html')),
    url(r'^auth/', include('auth.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^shoppingcart/', include('shoppingcart.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # The line below enables admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # django-rq panel
    url(r'^django-rq/', include('django_rq.urls')),
)
