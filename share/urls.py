from django.urls import path
from django.conf.urls import url
from . import views, forms

urlpatterns = [
    path("", views.index, name="index"), # Both of these lines work
    # note per https://stackoverflow.com/questions/4951203/what-are-the-default-urls-for-djangos-user-authentication-system
    # patterns() is deprecated and url() should be used instead
    # url(r'^$', views.index, name='index'),
    path("share/summary", views.summary, name="summary"),
    path("share/sign_up", views.sign_up, name="sign_up"),
    path("member_profile/update/", views.Member_profileUpdate.as_view(), name="update_member_profile_form"), # Needed 5/26/20 to get past NoReverseMatch Error
    path("member_profile/update/<int:pk>", views.Member_profileUpdate.as_view(), name="update_member_profile_form"),
    # path('provisions/', views.ProvisionListView.as_view(), name='provision_list'), #Commented out 5/2/20 - not worth the trouble
    path("provision/create/", views.ProvisionCreate.as_view(), name="create_provision_form"),
    path("provisions/<int:pk>/", views.ProvisionDetailView.as_view(), name="provision_detail"),
    path("provision/update/", views.ProvisionUpdate.as_view(), name="update_provision_form"), # Needed 5/26/20 to get past NoReverseMatch Error
    path("provision/update/<int:pk>", views.ProvisionUpdate.as_view(), name="update_provision_form"),
    path("need/create/", views.NeedCreate.as_view(), name="need_form"),
    path("needs/<int:pk>/", views.NeedDetailView.as_view(), name="need_detail"),
    path("need/update/", views.NeedUpdate.as_view(), name="update_need_form"), # Needed 5/26/20 to get past NoReverseMatch Error
    path("need/update/<int:pk>", views.NeedUpdate.as_view(), name="update_need_form"),
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
    path("end_membership/", views.end_membership, name="end_membership"),
    path("end_membership/<int:pk>/", views.end_membership, name="end_membership"),
    path("action_item/update/", views.Action_itemUpdate.as_view(), name="update_action_item_form"),
    path("action_item/update/<int:pk>/", views.Action_itemUpdate.as_view(), name="update_action_item_form"),
    path("all_items/<str:item_type>/", views.all_items, name="all_items"),
    path("all_items/", views.all_items, name="all_items"),
    path("logged_out/", views.logged_out, name="logged_out"),
    ]
