from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', 'auth.views.register', name="register"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
]