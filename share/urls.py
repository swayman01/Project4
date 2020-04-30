# Add as needed
from django.urls import path
from django.conf.urls import url
from . import views
# from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"), # Both of these lines work
    # not per https://stackoverflow.com/questions/4951203/what-are-the-default-urls-for-djangos-user-authentication-system
    # patterns() is deprecated and url() should be used instead
    # url(r'^$', views.index, name='index'),
    path("share/summary", views.summary, name="summary"), # This worked
    path("share/sign_up", views.sign_up, name="sign_up"),
    # url(r'^$', views.summary, name='summary'), This doesn't work
    ]
