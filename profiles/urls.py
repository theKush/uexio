from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^public/(?P<username>.*)$', 'profile', name="profile"),
    url(r'^review/(?P<username>.*)$', 'review_seller', name="review_seller"),
    url(r'^edit/$', 'edit_profile', name="edit_profile"),
    url(r'^library/$', 'library', name="library"),
    url(r'^listings/$', 'listings', name="listings"),
    url(r'^edit_password/$', 'edit_password', name="edit_password"),
)
