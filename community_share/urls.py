"""community_share URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Add as needed
# from django.contrib.auth.views import LogoutView
from share import views as core_views
from django.conf.urls import url
#from django.views.generic.base import TemplateView # see https://dev.to/jonesoncorners/series-login-logout-authentication-in-django-part-i-4gf4

urlpatterns = [
    path('', include('share.urls')),
    path('admin/', admin.site.urls),
    #Add Django site authentication urls (for login, logout, password management)
    path('registation/', include('django.contrib.auth.urls')),
    # Add as needed from Projedt3
    # # see https://dev.to/jonesoncorners/series-login-logout-authentication-in-django-part-i-4gf4
    #path('', TemplateView.as_view(template_name ='home.html'), name = 'home'),
]
# print("33 community share urls", urlpatterns)
