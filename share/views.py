# Reference for editing/creating Provisions https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
import os#, datetime
import json
from django.urls import reverse, reverse_lazy #, path
# from django.views.generic.list import ListView
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView #, DeleteView
from django.template import Context, Template, loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate #,login, logout #from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.contrib.auth.decorators import login_required #, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from share.forms import Sign_upForm, Member_profileForm
# reference: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/
from django.core.mail import send_mail
# reference: https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
from share.models import Member_profile, Provision, Need

# Add as needed
# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from django.views.generic import TemplateView
# from django.views.generic.detail import DetailView
# from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth import login, logout, authenticate # 9/28/ 19 from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# from django.contrib.auth.forms import UserCreationForm # 9/28/ 19 from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# from datetime import date, datetime
# import requests
# import itertools
# from django.template import Context, Template, loader
# from django.views.decorators.csrf import csrf_exempt # from https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
# from decimal import Decimal

# For sign_up
# From https://github.com/egorsmkv/simple-django-login-and-register
# TODO: Delete unneeded forms
# from .forms import (
#     SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
#     RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
#     ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm, ChangeEmailForm,
# )

# Another Reference: https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67

#SOMEDAY fix favicon.ico error
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    # If request,user.is_authenticated go to summary()
    context = {
    'user_is_authenticated':request.user.is_authenticated,
    }
    return render(request, 'share/index.html/',context)


def sign_up(request):
    """ Potential Members sign up here. They are enrolled after Administrator approval
        They can update their material from edit profile
        """
    if request.method == 'POST':
        form_errorsSTR = ""
        sign_up_a_form = Sign_upForm(data=request.POST)
        sign_up_b_form = Member_profileForm(data=request.POST)
        x1 = json.dumps(sign_up_a_form.errors)
        x2 = sign_up_a_form.non_field_errors
        x3 = json.dumps(sign_up_b_form.errors)
        x4 = sign_up_b_form.non_field_errors
        # print("97 _form.errors",sign_up_a_form.errors,"\nx1\n",x1,"\nx3\n",x3)
        # print("98 non_field errors",x2,x4)
        if sign_up_a_form.is_valid() and sign_up_b_form.is_valid():
            # print("88: sign_up_b_form", sign_up_b_form.cleaned_data)
            username = sign_up_a_form.cleaned_data.get('username')
            password = sign_up_a_form.cleaned_data.get('password1')
            email = sign_up_a_form.cleaned_data.get('email')
            first_name = sign_up_a_form.cleaned_data.get('first_name')
            last_name = sign_up_a_form.cleaned_data.get('last_name')
            phone_number = sign_up_b_form.cleaned_data.get('phone_number')
            city = sign_up_b_form.cleaned_data.get('city')
            state = sign_up_b_form.cleaned_data.get('state')
            zip_code = sign_up_b_form.cleaned_data.get('zip_code')
            member_bio = sign_up_b_form.cleaned_data.get('member_bio')
            if  email == "" and phone_number == "":
                x1STR = {"contact_info": ["Provide email or text number"]}
                x1 = json.dumps(x1STR)
                context = {
                    'sign_up_a_form':sign_up_a_form,
                    'sign_up_b_form':sign_up_b_form,
                    'sign_up_a_form_non_field_errors':x2,
                    'form_errorsJSONSTR':x1,
                }
                return render(request, 'share/sign_up.html/', context=context)

            user = User.objects.create_user(username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            member_id = User.objects.get(username=username).id
            print ("104",username)
            member_profile_new = Member_profile(
                member_id = member_id,
                phone_number = phone_number,
                city = city,
                state = state,
                zip_code = zip_code,
                member_bio = member_bio,
                name = username
            )
            member_profile_new.save()
            print("126 ready to send email", username)
            email_message = username + ' has requested to join. Please review application, login to admin and check Is approved box'
            send_mail('New Applicant', email_message, 'achoo4259@yahoo.com', ['achoo4259@yahoo.com',],fail_silently=False)
            context = {
            "error_message":"Approval request has been sent to Admin"
            }
            # Put logout screen with message to wait for admin approval
            return render(request, 'registration/logged_out.html/',context)
        else:
            context = {
                'sign_up_a_form':sign_up_a_form,
                'sign_up_b_form':sign_up_b_form,
                'sign_up_a_form_non_field_errors':x2,
                'form_errorsJSONSTR':x1,
            }
            return render(request, 'share/sign_up.html/', context=context)

# TODO Format phone_number
            # MAYBE: do something similar for city, state, zipcode
            # Note that this requires zip code lookups

@login_required
def summary(request):
    print("summary Line 136:",request)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_name = user.username
    # member_id = Provision.member_id
    my_profile = Member_profile.objects.filter(member_id=user.id).first()
    if my_profile == None:
        print("158: TODO Member missing profile")
        context = {
        "error_message": "You do not have a profile. Please contact Community Share Administrator"
        }
        return render(request, 'registration/logged_out.html',context)
    if my_profile.is_approved != True:
        context = {
        "error_message": "You have not yet been approved. Please contact \
        Community Share Administrator if you have been registered for more than one day."
        }
        return render(request, 'registration/logged_out.html',context)
    # print("156: ",user_id,user,user_name,my_profile)
    # TODO add check for null
    provisionlast = Provision.objects.last()
    print("155",provisionlast)
    print("157",Provision.objects.last().member_id)
    if int(Provision.objects.last().member_id)==0:
        print("158 creating new provision")
        create_provision(request)
    if int(Need.objects.last().member_id)==0:
        print("161 creating new need")
        create_need(request)
    if my_profile.is_moderator == True:
        provisions = list(Provision.objects.all())
        needs = list(Need.objects.all())
    else:
        provisions = list(Provision.objects.filter(member_id=user_id))
        needs = list(Need.objects.filter(member_id=user_id))
        print("159",len(provisions),provisions[len(provisions)-1].name, provisions[len(provisions)-1].member_id)
    context = {
    'user_is_authenticated':request.user.is_authenticated,
    'user_is_approved':my_profile.is_approved,
    'my_profile':my_profile,
    'provisions': provisions,
    'needs': needs,
    }
    print("views 173: TODO fix if statement for logged out")
    if True:
        return render(request, 'share/summary.html/',context)
    else:
        return render(request, 'registration/logged_out.html',context)


def create_provision(request):
    """This adds the member_id to the latest provision"""
    print("177 create_provision")
    user_id = request.user.id
    # Let admin check for provisions with non-existent users
    provisions = list(Provision.objects.all())
    last_provision_id = provisions[len(provisions)-1].id
    Provision.objects.filter(id=last_provision_id).update(member_id=user_id)
    # provisions = list(Provision.objects.all())
    # context = {
    # 'provisions': provisions,
    # }
    return #render(request, 'share/summary.html/',context)


class ProvisionCreate(CreateView):
    print("191 ProvisionCreate")
    model = Provision
    fields = ['name', 'type', 'frequency', 'expiration_date']
    success_url = reverse_lazy('summary')


class ProvisionUpdate(UpdateView):
    model = Provision
    # fields = ['name', 'type', 'frequency', 'expiration_date','status']
    # TODO fix provided_to column
    fields = ['name', 'type', 'frequency', 'expiration_date','status','provided_to']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


class ProvisionDetailView(generic.DetailView):
    model = Provision
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProvisionDetailView, self).get_context_data(**kwargs)
        return
###########################
class NeedCreate(CreateView):
    model = Need
    fields = ['name', 'type', 'due_date','background_info']
    success_url = reverse_lazy('summary')


class NeedUpdate(UpdateView):
    model = Need
    # TODO fix provided_from column
    fields = ['name', 'type', 'due_date','background_info','provided_from']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


class NeedDetailView(generic.DetailView):
    model = Need
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(NeedDetailView, self).get_context_data(**kwargs)
        return


def create_need(request):
    """This adds the member_id to the latest provision"""
    print("245 create_provision")
    user_id = request.user.id
    # Let admin check for needs with non-existent users
    needs = list(Need.objects.all())
    last_need_id = needs[len(needs)-1].id
    Need.objects.filter(id=last_need_id).update(member_id=user_id)
    # needs = list(Need.objects.all())
    # context = {
    # 'provisions': provisions,
    # }
    return #render(request, 'share/summary.html/',context)


###########################
class Member_profileCreate(CreateView):
    model = Member_profile
    fields = ['member_id', 'phone_number', 'city', 'state','zip_code', 'member_bio']
    success_url = reverse_lazy('summary')

### Utilities ###
def clean_orphan_member_profiles():
    # TODO make less manual
    user_ids = []
    users = User.objects.all()
    print("224",users)
    for user in users:
        user_id = User.objects.get(username=user).id
        print("225 ", user, user_id)
        print("227 ")
        user_ids.append(user_id)
    print("230 ", user_ids)
    member_profiles = Member_profile.objects.all()
    for member_profile in member_profiles:
        print("233 ", member_profile)
        #member_id = Member_profile.objects.get(username=user).id
    #     print("233 ", user_ids.count(test_list))
    return

#clean_orphan_member_profiles()



# class ProvisionListView(ListView): Commented out 5/2/2020 - not worth the trouble
#
#     model = Provision
#     paginate_by = 20  # if pagination is desired
#
#     def get_context_data(self, **kwargs):
#         context = super(ProvisionListView,self).get_context_data(**kwargs)
#         contex_object_name = 'provision_list'
#         context['now'] = timezone.now()
#         return context
