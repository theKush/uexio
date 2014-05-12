from django.conf.urls import url

urlpatterns = [
    # url routing to navigate to register page
    url(r'^register/$', 'auth.views.register', name="register"),
    # url routing to navigate to login page
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    # url routing to logout an user
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
]
