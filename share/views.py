import os#, datetime
import json
from django.shortcuts import render
from share.models import Member_profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.contrib.auth import authenticate #,login, logout #from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.template import Context, Template, loader
from share.forms import Sign_upForm, Member_profileForm
# reference: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/

from django.core.mail import send_mail
# reference: https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html

# Add as needed
# from django.shortcuts import render, get_object_or_404, redirect
# from django.views import generic
# from django.utils import timezone
# from django.views.generic.list import ListView
# from django.views.generic import TemplateView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse, reverse_lazy, path
# from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth import login, logout, authenticate # 9/28/ 19 from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# from django.contrib.auth.forms import UserCreationForm # 9/28/ 19 from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# from orders.models import Regularpizza, Sicilianpizza, Topping, Salad, Pasta
# from orders.models import Sub, Dinnerplatter, Order, User, Rating

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    # If request,user.is_authenticated go to summary()
    context = {
    'user_is_authenticated':request.user.is_authenticated,
    }
    return render(request, 'share/index.html/',context)


def summary(request):
    print("summary Line 76:",request)
    # print("summary Line 45:",request, user.is_authenticated)
    context = {

    }
    return render(request, 'share/summary.html/',context)


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
# TODO Modify html
# TODO Format phone_number
            # MAYBE: do something similar for city, state, zipcode
            # Note that this requires zip code lookups

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
            member_profile_new = Member_profile(
                member_id = member_id,
                phone_number = phone_number,
                city = city,
                state = state,
                zip_code = zip_code,
                member_bio = member_bio
            )
            member_profile_new.save()
            print("126 ready to send email", username)
            email_message = username + ' has requested to join. Please review application, login to admin and check Is approved box'
            send_mail('New Applicant', email_message, 'achoo4259@yahoo.com', ['achoo4259@yahoo.com',],fail_silently=False)
            context = {

            }
            # Put render next screen here
            return render(request, 'share/summary.html/',context)
        else:
            # TODO set up flag for initial view
            # print("114: sign_up_a_form.errors", sign_up_a_form.errors)
            # form_errorsJSONSTR = form_errors(sign_up_a_form.errors)
            # print("116 form is not valid: ",sign_up_a_form.errors,"\n",x1)
            context = {
                'sign_up_a_form':sign_up_a_form,
                'sign_up_b_form':sign_up_b_form,
                'sign_up_a_form_non_field_errors':x2,
                'form_errorsJSONSTR':x1,
            }
            return render(request, 'share/sign_up.html/', context=context)


def sign_upExperiments(request):
    """ Potential Members sign up here. They are enrolled after Administrator approval
        They can update their material from edit profile
        """

    if request.method == 'POST':
        form_errorsSTR = ""
        # sign_up_a_form = Sign_upForm(data=request.POST)
        sign_up_a_form = modelformset_factory(UserCreationForm, fields=('username','password','first_name','last_name','email'))
        sign_up_b_form = Member_profileForm(data=request.POST)
        x1 = json.dumps(sign_up_a_form.errors)
        x2 = sign_up_a_form.non_field_errors
        x3 = json.dumps(sign_up_b_form.errors)
        print("97 _form.errors",sign_up_a_form.errors,"\nx1\n",x1,"\nx1\n",sign_up_b_form.errors,"\nx1\n",x3)
        #if sign_up_a_form.is_valid() and sign_up_b_form.is_valid():
        if sign_up_a_form.is_valid():
            username = sign_up_a_form.cleaned_data.get('username')
            password = sign_up_a_form.cleaned_data.get('password1')
            #TODO Add checks for Zip Code or Address
            email = sign_up_a_form.cleaned_data.get('email')
            first_name = sign_up_a_form.cleaned_data.get('first_name')
            last_name = sign_up_a_form.cleaned_data.get('last_name')
            user = User.objects.create_user(username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            context = {
                'formtest':sign_up_a_form,

            }
            return render(request, 'share/summary.html/',context)
        else:
            # print("114: sign_up_a_form.errors", sign_up_a_form.errors)
            # form_errorsJSONSTR = form_errors(sign_up_a_form.errors)
            # print("116 form is not valid: ",form_errorsJSONSTR,"\n",sign_up_a_form.errors,"\n",x2)
            context = {
                'sign_up_a_form':sign_up_a_form,
                'sign_up_b_form':sign_up_b_form,
                'sign_up_a_form_non_field_errors':x2,
                # 'form_errorsJSONSTR':form_errorsJSONSTR,
                # TODO add form_b errors
                'form_errorsJSONSTR':x1,

            }
            return render(request, 'share/sign_up.html/', context=context)


def form_errors(form_errors):
    """Input: Dictionary of errors
       Output: JSON string suitable for passing to javascript.
    """
    print("122: form_errors",form_errors)
    errors = ""
    if len(form_errors) > 0:
        for key, value in form_errors.items():
            print("124 value", value)
            errors = errors + value +"\n"
        errorsJSONSTR =json.dumps(errors)
        errorsJSONSTR = errorsJSONSTR.replace("'",'"')
        print("136 errors:",errorsJSONSTR)
    return errorsJSONSTR




    #TODO Add delete account to update profile page
    # Gather information
        # Validate data in Javascript
            # Make sure format is correct
            # Convert telephone number to common format
        # Pass data to Python
        # Make sure passwords match ()
    # Create user in user model
    # Create profile in Memberprofile
    # Send email(s) to Administrator(s) use field in user model
    # Routine for Administrator to approve/reject
        # Approve, update model and email reply
        # Disapprove, Add note to Bio section saying why
        # Send optional email to applicant with a different explanation


    #TODO use is_administr
    #NEXT: fill-in city and state default from zip code,
    #don't show until zip code is filled in


# Sample Code from  https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67
# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 profile.profile_pic = request.FILES['profile_pic']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors,profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#     return render(request,'dappx/registration.html',
#                           {'user_form':user_form,
#                            'profile_form':profile_form,
#                            'registered':registered})

# sample code from https://github.com/egorsmkv/simple-django-login-and-register
# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = settings.SIGN_UP_FIELDS
#
#     email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#
#         user = User.objects.filter(email__iexact=email).exists()
#         if user:
#             raise ValidationError(_('You can not use this email address.'))
#
#         return email
