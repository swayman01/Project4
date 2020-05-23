# Add as needed
from django.urls import path
from django.conf.urls import url
from . import views
# from share.views import ProvisionListView


urlpatterns = [

]
# from django.conf import settings
#TODO make all double quotes
urlpatterns = [
    path("", views.index, name="index"), # Both of these lines work
    # not per https://stackoverflow.com/questions/4951203/what-are-the-default-urls-for-djangos-user-authentication-system
    # patterns() is deprecated and url() should be used instead
    # url(r'^$', views.index, name='index'),
    path("share/summary", views.summary, name="summary"), # This worked
    path("share/sign_up", views.sign_up, name="sign_up"),
    # path('provisions/', views.ProvisionListView.as_view(), name='provision_list'), #Commented out 5/2/20 - not worth the trouble
    # path('provision/create_provision/', views.create_provision(), name='create_provision'),
    path("provision/create/", views.ProvisionCreate.as_view(), name="create_provision_form"),
    path("provisions/<int:pk>/", views.ProvisionDetailView.as_view(), name="provision_detail"),
    path("provision/<int:pk>/update/", views.ProvisionUpdate.as_view(), name="update_provision_form"),
    path("need/create/", views.NeedCreate.as_view(), name="need_form"),
    path("needs/<int:pk>/", views.NeedDetailView.as_view(), name="need_detail"),
    path("need/<int:pk>/update/", views.NeedUpdate.as_view(), name="update_need_form"),
    path("match_need_to_provision", views.match_need_to_provision, name="match_need_to_provision"),
    path("match_need_to_provision/<int:pk>/<int:member_id>/", views.match_need_to_provision, name="match_need_to_provision"),
    path("match_provision_to_need", views.match_provision_to_need, name="match_provision_to_need"),
    path("match_provision_to_need/<int:pk>/<int:member_id>/", views.match_provision_to_need, name="match_provision_to_need"),
    path("need_contact_info/", views.need_contact_info, name="need_contact_info"), # for debugging urls
    path("need_contact_info/<int:pk1>/<int:pk2>/", views.need_contact_info, name="need_contact_info"),
    path("provision_contact_info/", views.provision_contact_info, name="provision_contact_info"), # for debugging urls
    path("provision_contact_info/<int:pk1>/<int:pk2>/", views.provision_contact_info, name="provision_contact_info"),
    path("share/need_not_needed", views.need_not_needed, name="need_not_needed"),
    path("status_update/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>/", views.status_update, name="status_update"),
    path("status_update/", views.status_update, name="status_update"),
    ]
# print("33 urls.py",urlpatterns)
