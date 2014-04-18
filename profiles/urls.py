from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^$', 'profile', name="profile"),
    url(r'^edit/$', 'edit_profile', name="edit_profile"),
    url(r'^library/$', 'library', name="library"),
    url(r'^listings/$', 'listings', name="listings"),
)
