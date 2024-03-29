from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^public/(?P<username>.*)$', 'profile', name="profile"),
    url(r'^review/(?P<username>.*)$', 'review_seller', name="review_seller"),
    url(r'^edit/$', 'edit_profile', name="edit_profile"),
    url(r'^library/$', 'library', name="library"),
    url(r'^listings/$', 'listings', name="listings"),
    url(r'^mypurchases/$', 'mypurchases', name="mypurchases"),
    url(r'^mysolditems/$', 'mysolditems', name="mysolditems"),
    url(r'^edit_password/$', 'edit_password', name="edit_password"),
    url(r'^password_change_done/$', 'password_change_done', name="password_change_done"),
)
