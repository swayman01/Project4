# References for querying
# https://docs.djangoproject.com/en/3.0/ref/models/querysets/#queryset-api
#  Try .values for python queries
# https://docs.djangoproject.com/en/3.0/ref/models/querysets/#field-lookups
#  Try .contains, .explain()

# Reference for editing/creating Provisions https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
import json, os, operator, datetime, pytz, re
from datetime import date, datetime
# reference http://bradmontgomery.blogspot.com/2009/06/adding-q-objects-in-django.html
# and https://stackoverflow.com/questions/45253994/django-filter-with-or-statement
from django import forms
from django.db.models import Q
from django.urls import reverse, reverse_lazy #, path
# from django.views.generic.list import ListView
from django.views import generic
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView #, DeleteView
from django.template import Context, Template, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout #,login #from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.contrib.auth.decorators import login_required #, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from share.forms import Sign_upForm, Member_profileForm, phone_number_checker
# reference: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/
from django.core.mail import send_mail
# reference: https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
from share.models import Member_profile, Provision, Need, Action_item

# Second solution from https://stackoverflow.com/questions/298772/django-template-variables-and-javascript
# from django.utils.safestring import mark_safe
# from django.template import Library
# register = Library()
# @register.filter(is_safe=True)
# def js(obj):
#     return mark_safe(json.dumps(obj))
# Add as needed

# from django.utils import timezone
# from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
        if sign_up_a_form.is_valid() and sign_up_b_form.is_valid():
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
                    'sign_up_b_form_errors':x3,
                    'form_errorsJSONSTR':x1,
                    }
                return render(request, 'registration/sign_up.html/',context)
            user = User.objects.create_user(username,email=email, password=password,first_name=first_name,last_name=last_name)
            phone_number = phone_number_checker(phone_number)[1]
            user.save()
            member_id = User.objects.get(username=username).id
            # Check for existing member_profile (for those who left the community and are rejoinning)
            existing_member_profile =  Member_profile.objects.filter(name=username)
            if existing_member_profile != None:
                print ("108 Profile does notexist, now what?")
                email_message = username + ' has two member_profiles. Please delete one of them'
                send_mail('New Applicant', email_message, 'achoo4259@yahoo.com', ['achoo4259@yahoo.com',],fail_silently=False)
                action_item_new = Action_item(
                    name = "Delete Duplicate Profile",
                    owner = "Moderator",
                    status = "Open",
                    description = email_message,
                 )
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
            email_message = username + ' has requested to join. Please review application, login to admin and check Is approved box'
            send_mail('New Applicant', email_message, 'achoo4259@yahoo.com', ['achoo4259@yahoo.com',],fail_silently=False)
            context = {
            "error_message":"Approval request has been sent to Admin"
            }
            action_item_new = Action_item(
                name = "Approve New Member Request",
                owner = "Moderator",
                status = "Open",
                description = email_message,
             )
            action_item_new.save()
            logout(request)
            return render(request, 'registration/logged_out.html/',context)
            # return render(request, 'share/sign_up.html/', context=context)
        else:
            print("109 form not valid")
            phone_number_errorJSON = json.loads(sign_up_b_form.errors.as_json())
            print("111",phone_number_errorJSON)
            try:
                print("156",phone_number_errorJSON['phone_number'][0]['message'])
                phone_number_errorJSON = phone_number_errorJSON['phone_number'][0]
                phone_number_error_coded =  {"message":[phone_number_errorJSON["message"]]}
                print("159",phone_number_error_coded)
                sign_up_a_form.errors.update(phone_number_error_coded)
                print("161",sign_up_a_form.errors)
                x1 = json.dumps(sign_up_a_form.errors)
            except:
                phone_number_errorJSONSTR = ""
            context = {
                'sign_up_a_form':sign_up_a_form,
                'sign_up_b_form':sign_up_b_form,
                'sign_up_a_form_non_field_errors':x2,
                'form_errorsJSONSTR':x1,
                # 'phone_number_error':'TODOdelete after debugging'
                }
            return render(request, 'share/sign_up.html/', context=context)

# SOMEDAY incorporate zip code lookups

@login_required
def summary(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_name = user.username
    my_profile = Member_profile.objects.filter(member_id=user.id).first()
    if my_profile == None:
        context = {
        "error_message": "You do not have a profile. Please contact Community Share Administrator"
        }
        logout(request)
        return render(request, 'registration/logout',context)
        # return render(request, 'registration/logged_out.html',context)
    if my_profile.is_approved != True:
        error_message = "You have not yet been approved. Is "
        error_message = error_message + (str(user.email))
        error_message = error_message + " your correct email? "
        error_message = error_message + "Please contact if it isn't or "
        error_message = error_message + "if you have been waiting more than a day. "
        context = {
        "error_message": error_message
        }
        logout(request)
        return render(request, 'registration/logged_out.html',context)
    provisionlast = Provision.objects.last()
    if int(Provision.objects.last().member_id)==0:
        create_provision(request)
    if int(Need.objects.last().member_id)==0:
        create_need(request)
    if my_profile.is_moderator == True:
        provisions = Provision.objects.all()
        needs = Need.objects.all()
        for provision in provisions:
            provision.expiration_date = format_date(provision.expiration_date)
        for need in needs:
            need.due_date = format_date(need.due_date)
    else:
        provisions = Provision.objects.filter(member_id=user_id). \
        filter(Q(status='Available')|Q(status='Pending')| \
        Q(status='available')|Q(status='pending'))
        # provisions = Provision.objects.filter(member_id=user_id) # For Debugging
        for provision in provisions:
            provision.expiration_date = format_date(provision.expiration_date)
        needs = Need.objects.filter(member_id=user_id). \
        filter(Q(status='Open')|Q(status='open')|Q(status='Pending')|Q(status='pending'))
        for need in needs:
            need.due_date = format_date(need.due_date)
    expiration_due_date_check(request,provisions,needs)
    provisions_active = Provision.objects.filter(member_id=user_id) \
    .filter(Q(status='Pending')|Q(status='pending'))
    provisions_activeLIST = []
    for provision in provisions_active:
        try:
            provided_to_name = User.objects.get(id=provision.provided_to).username
            provisionLIST = [provision.name,provided_to_name,provision.status,provision.id,provision.provided_to]
            provisions_activeLIST.append(provisionLIST)
        except:
            provision.status="Available"
            provision.save()
    needs_active = Need.objects.filter(member_id=user_id).filter(Q(status='Pending')|Q(status='pending'))
    needs_activeLIST = []
    for need in needs_active:
        try:
            provided_from_name = User.objects.get(id=need.provided_from).username
            # print("196", User.objects.get(id=need.provided_from))
            needLIST = [need.name,provided_from_name,need.status,need.id,need.provided_from]
            needs_activeLIST.append(needLIST)
        except:
            need.status="Open"
            need.save()
    action_items_open = Action_item.objects.filter(status="Open")
    context = {
    'user_is_authenticated':request.user.is_authenticated,
    'user_is_approved':my_profile.is_approved,
    'my_profile':my_profile,
    'provisions': provisions,
    'provisions_active': provisions_activeLIST,
    'needs_active': needs_activeLIST,
    'needs': needs,
    'action_items_open':action_items_open,
    }
    return render(request, 'share/summary.html/',context)


@login_required
def all_items(request,item_type):
    user_id = request.user.id
    if item_type == "action_items":
        headerLIST = ["Name","Owner","Status","Description"];
        headerJSON = json.dumps(headerLIST)
        itemsLIST = []
        for item in Action_item.objects.all():
            itemLIST = [item.name,item.owner,item.status,item.description]
            itemsLIST.append(itemLIST)
        itemsJSON = json.dumps(itemsLIST)
        print("257",itemsJSON)
        context = {
        'title':'All Action Items',
        'items':itemsJSON,
        'header': headerJSON
            }
    if item_type == "provisions":
        headerLIST = ["Provision","Type","Status","Frequency","Expiration Date"];
        headerJSON = json.dumps(headerLIST)
        itemsLIST = []
        for item in Provision.objects.filter(member_id=user_id):
            expiration_date = format_date(item.expiration_date)
            itemLIST = [item.name,item.type,item.status,item.frequency,expiration_date]
            itemsLIST.append(itemLIST)
        itemsJSON = json.dumps(itemsLIST)
        context = {
        'title':'All My Provisions',
        'items':itemsJSON,
        'header': headerJSON
            }
    if item_type == "needs":
        headerLIST = ["Need","Type","Status","Due Date"];
        headerJSON = json.dumps(headerLIST)
        itemsLIST = []
        for item in Need.objects.filter(member_id=user_id):
            due_date = format_date(item.due_date)
            itemLIST = [item.name,item.type,item.status,due_date]
            itemsLIST.append(itemLIST)
        itemsJSON = json.dumps(itemsLIST)
        context = {
        'title':'All My Needs',
        'items':itemsJSON,
        'header': headerJSON
            }
    return render(request, 'share/all_items.html/',context)


def format_date(date_in):
    """This function returns date in the desired format"""
    if date_in!=None:
        try:
            date_out = date_in.strftime("%b %d, %Y")
        except:
            date_in = datetime.strptime(date_in, "%b %d, %Y")
            date_out = date_in.strftime("%Y-%m-%d")
        return date_out


@login_required
def create_provision(request):
    """This adds the member_id to the latest provision and clears time from the
    expiration_date"""
    user_id = request.user.id
    # Let admin check for provisions with non-existent users
    provisions = list(Provision.objects.all())
    provisions = Provision.objects.all()
    last_provision_id = provisions[len(provisions)-1].id
    Provision.objects.filter(id=last_provision_id).update(member_id=user_id)
    return


@login_required
def create_need(request):
    """This adds the member_id to the latest provision"""
    user_id = request.user.id
    # Let admin check for needs with non-existent users
    needs = list(Need.objects.all())
    last_need_id = needs[len(needs)-1].id
    Need.objects.filter(id=last_need_id).update(member_id=user_id)
    return


@login_required
def match_need_to_provision(request,pk,member_id):
    provision = Provision.objects.filter(id=pk).first()
    provision.expiration_date = format_date(provision.expiration_date)
    provisionSET = set(provision.name.lower().split())
    needs = Need.objects.filter(type=provision.type).filter(~Q(member_id=member_id)). \
    filter(Q(status='Open')|Q(status='open')|Q(status='Pending')|Q(status='pending'))
    needsLIST = []
    for need in needs:
        needSET = set(need.name.lower().split())
        common_words = provisionSET.intersection(needSET)
        print("240",common_words)
        if len(common_words)>0:
            needsLIST.append(need)
    # needs = Need.objects.filter(type=provision.type) # for debugging
    for need in needs:
        need.due_date = format_date(need.due_date)
    context = {
    'provision':provision,
    # 'needs': needs,
    'needs': needsLIST,
    }
    return render(request, 'share/match_need_to_provision.html/',context)


@login_required
def match_provision_to_need(request,pk,member_id):
    print("259",member_id)
    need = Need.objects.filter(id=pk).first()
    need.due_date = format_date(need.due_date)
    needSET = set(need.name.lower().split())
    provisions = Provision.objects.filter(type=need.type).filter(~Q(member_id=member_id)). \
    filter(Q(status='Available')|Q(status='available')|Q(status='Pending')|Q(status='pending'))
    #provisions = Provision.objects.filter(type=need.type) #Debug
    provisionsLIST = []
    for provision in provisions:
        provisionSET = set(provision.name.lower().split())
        common_words = provisionSET.intersection(needSET)
        if len(common_words)>0:
            provisionsLIST.append(provision)
    for provision in provisions:
        provision.expiration_date = format_date(provision.expiration_date)
    context = {
    'provisions':provisionsLIST,
    'need': need,
    }
    return render(request, 'share/match_provision_to_need.html/',context)


@login_required
def need_contact_info(request,pk1,pk2):
    need = Need.objects.get(id=pk1)
    member_id = Need.objects.get(id=pk1).member_id
    print("228 need,member_id",need,member_id)
    user_check = User.objects.filter(id=member_id).count()
    if user_check<1:
        Need.objects.filter(id=pk1).update(status="Retracted")
        context = {
        'need': need,
        'error': 'has been retracted'
        }
        return render(request,'share/need_not_needed.html/',context)
    user = User.objects.filter(id=member_id)
    contact = Member_profile.objects.filter(member_id=member_id).first()
    provision = Provision.objects.filter(id=pk2).first()
    provision.expiration_date = format_date(provision.expiration_date)
    context = {
    'provision':provision,
    'need': need,
    "contact":contact,
    "user":user,
    }
    return render(request, 'share/need_contact_info.html/',context)


@login_required
def provision_contact_info(request,pk1,pk2):
    provision = Provision.objects.get(id=pk1)
    member_id = Provision.objects.get(id=pk1).member_id
    user_check = User.objects.filter(id=member_id).count()
    if user_check<1:
        Provision.objects.filter(id=pk1).update(status="Retracted")
        print("319 retracted",pk1,pk2)
        context = {
        'provision': provision,
        'error': 'no longer available'
        }
        return render(request,'share/provision_not_available.html/',context)
    user = User.objects.filter(id=member_id)
    contact = Member_profile.objects.filter(member_id=member_id).first()
    need = Need.objects.filter(id=pk2).first()
    need.due_date = format_date(need.due_date)
    context = {
    'provision':provision,
    'need': need,
    "contact":contact,
    "user":user,
    }
    return render(request, 'share/provision_contact_info.html/',context)


@login_required
def need_not_needed(request):
    context = {
    "error":"Need retracted"
    }
    return render(request, 'share/need_contact_info.html/',context)


@login_required
def status_update(request,pk1,pk2,pk3,pk4):
    """Update status change:
    pk1=1 for provision, 2 for need
    pk2 is id for a provision or a need
    pk3=1 is for open or available, 2 for pending, 3 for provided, 5 for retracted
    pk4 is receiving member id"""
    # print("357, pk1, pk2, pk3, pk4", pk1, pk2, pk3, pk4)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    my_profile = Member_profile.objects.filter(member_id=user.id).first()
    if pk1==1:
        if pk3==1:
            x = Provision.objects.filter(id=pk2).update(status="Available")
            Provision.objects.filter(id=pk2).update(provided_to=None)
        if pk3==2:
            Provision.objects.filter(id=pk2).update(status="Pending")
            Provision.objects.filter(id=pk2).update(provided_to=pk4)
        if pk3==3:
            x = Provision.objects.filter(id=pk2).update(status="Provided")
            Provision.objects.filter(id=pk2).update(status="Provided")
            Provision.objects.filter(id=pk2).update(provided_to=pk4)
        if pk3==5:
            Provision.objects.filter(id=pk2).update(status="Retracted")
            Provision.objects.filter(id=pk2).update(provided_to=None)
    if pk1==2:
        if pk3==1:
            # print("394 Need doesn't match")
            x = Need.objects.filter(id=pk2).update(status="Open")
            # print("396",x,Need.objects.filter(id=pk2))
            Need.objects.filter(id=pk2).update(provided_from=None)
        if pk3==2:
            # print("399 need contacted")
            x = Need.objects.filter(id=pk2).update(status="Pending")
            Need.objects.filter(id=pk2).update(provided_from=pk4)
            # print("402",x,Need.objects.filter(id=pk2))
        if pk3==3:
            x = Need.objects.filter(id=pk2).update(status="Provided")
            Need.objects.filter(id=pk2).update(status="Provided")
            Need.objects.filter(id=pk2).update(provided_from=pk4)
        if pk3==5:
            Need.objects.filter(id=pk2).update(status="Retracted")
            Need.objects.filter(id=pk2).update(provided_from=None)

    if my_profile.is_moderator == True:
        provisions = Provision.objects.all()
        # needs = list(Need.objects.all()) Commented out 5/20/20
        needs = Need.objects.all()
    else:
        # provisions_debug = Provision.objects.filter(member_id=user_id)
        # for provision in provisions_debug:
        #     print("315",provision.status,provision.member_id)
        # print ("314",provisions_debug)
        provisions = Provision.objects.filter(member_id=user_id) \
        .filter(Q(status='Available')|Q(status='Pending')
        |Q(status='available')|Q(status='pending'))
        for provision in provisions:
            provision.expiration_date = format_date(provision.expiration_date)
        needs = Need.objects.filter(member_id=user_id). \
        filter(Q(status='Open')|Q(status='open')|Q(status='Pending'))
        for need in needs:
            need.due_date = format_date(need.due_date)
    provisions = Provision.objects.filter(member_id=user_id)  \
    .filter(Q(status='Available')|Q(status='Pending'))
    needs = Need.objects.filter(member_id=user_id) \
    .filter(Q(status='Open')|Q(status='open')|Q(status='Pending'))
    # context = {
    #     'user_is_authenticated':request.user.is_authenticated,
    #     'user_is_approved':my_profile.is_approved,
    #     'my_profile':my_profile,
    #     'provisions': provisions,
    #     'needs': needs,
    #     }
# Added 6/5/2020
    provisions_active = Provision.objects.filter(member_id=user_id) \
    .filter(Q(status='Pending')|Q(status='pending'))
    provisions_activeLIST = []
    for provision in provisions_active:
        try:
            provided_to_name = User.objects.get(id=provision.provided_to).username
            provisionLIST = [provision.name,provided_to_name,provision.status,provision.id,provision.provided_to]
            provisions_activeLIST.append(provisionLIST)
        except:
            provision.status="Available"
            provision.save()
    needs_active = Need.objects.filter(member_id=user_id).filter(Q(status='Pending')|Q(status='pending'))
    needs_activeLIST = []
    for need in needs_active:
        try:
            provided_from_name = User.objects.get(id=need.provided_from).username
            # print("196", User.objects.get(id=need.provided_from))
            needLIST = [need.name,provided_from_name,need.status,need.id,need.provided_from]
            needs_activeLIST.append(needLIST)
        except:
            need.status="Open"
            need.save()
    action_items_open = Action_item.objects.filter(status="Open")
    context = {
    'user_is_authenticated':request.user.is_authenticated,
    'user_is_approved':my_profile.is_approved,
    'my_profile':my_profile,
    'provisions': provisions,
    'provisions_active': provisions_activeLIST,
    'needs_active': needs_activeLIST,
    'needs': needs,
    'action_items_open':action_items_open,
    }
# End Added 6/5/2020


    # summary(request) # This line did not eliminate the need for regenerating the context
    # return redirect('share/summary.html/',context) doesn't work 5/23/20
    # return render(request, summary) doesn't work 5/23/20
    return render(request, 'share/summary.html/',context)


@login_required
def action_item(request):
    print("469", request)
    context = {

    }
    return render(request, 'share/action_item.html/',context)


@login_required
def end_membership(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    username = user.username
    member_id = User.objects.get(username=username).id
    member_profile = Member_profile.objects.filter(member_id=member_id).first()
    member_profile_id = member_profile.id
    # Set open provisions and needs to retracted
    print("462", user_id, member_id, member_profile_id)
    my_open_needs = Need.objects.filter(~Q(member_id=member_profile_id)). \
    filter(Q(status='Open')|Q(status='open')|Q(status='Pending')|Q(status='pending'))
    my_open_needs.update(status="Retracted")
    my_open_provisions = Provision.objects.filter(~Q(member_id=member_profile_id)). \
    filter(Q(status='Available')|Q(status='available')|Q(status='Pending')|Q(status='pending'))
    my_open_provisions.update(status="Retracted")
    member_profile.is_approved=False
    member_profile.save()
    user.is_active=False
    user.save()
    error_message = "We are sorry to see you go. Our door is open. Contact the \
    System Administrator if you would like to rejoin"
    context = {
    "error_message":error_message,
    }
    return render(request, 'share/end_membership.html/',context)
    logout(request)
    print("482",request)
    return render(request, 'registration/logout',context)


@login_required
def expiration_due_date_check(request,provisions_queryset,needs_queryset):
    """This checks the expiration date and updates status if it is past"""
    utc = pytz.UTC
    current_time = datetime.now()
    provisions_queryset = provisions_queryset \
    .filter(Q(status='Available')|Q(status='Pending')
    |Q(status='available')|Q(status='pending'))
    needs_queryset = needs_queryset \
    .filter(Q(status='Open')|Q(status='Pending')
    |Q(status='open')|Q(status='pending'))
    for item in provisions_queryset:
        if item.expiration_date!=None:
            if current_time.replace(tzinfo=utc) > item.expiration_date.replace(tzinfo=utc):
                item.status = 'Expired'
                item.save()
                #print("394 updated status",item,current_time,item.expiration_date,item.status)
        for item in needs_queryset:
            if item.due_date!=None:
                if current_time.replace(tzinfo=utc) > item.due_date.replace(tzinfo=utc):
                    item.status = 'Expired'
                    item.save()
                    #print("401 updated status",item,current_time,item.due_date,item.status)
    return


class ProvisionCreate(CreateView):
    model = Provision
    fields = ['name', 'type', 'frequency', 'status','expiration_date']
    success_url = reverse_lazy('summary')


class ProvisionUpdate(UpdateView):
    model = Provision
    fields = ['name', 'type', 'frequency', 'expiration_date','status','provided_to']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


class ProvisionDetailView(generic.DetailView):
    model = Provision
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProvisionDetailView, self).get_context_data(**kwargs)
        return


class NeedCreate(CreateView):
    model = Need
    fields = ['name', 'type', 'due_date','status','background_info']
    success_url = reverse_lazy('summary')


class NeedUpdate(UpdateView):
    model = Need
    fields = ['name', 'type', 'due_date','status','provided_from','background_info']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


class NeedDetailView(generic.DetailView):
    model = Need
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(NeedDetailView, self).get_context_data(**kwargs)
        return


class Member_profileCreate(CreateView):
    model = Member_profile
    fields = ['member_id', 'phone_number', 'city', 'state','zip_code', 'member_bio']
    success_url = reverse_lazy('summary')


class Member_profileUpdate(UpdateView):
    model = Member_profile
    fields = ['phone_number', 'city','state','zip_code','member_bio']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


class Action_itemUpdate(UpdateView):
    model = Action_item
    fields = ['name', 'owner','status','description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('summary')


### Utilities ###
def clean_orphan_member_profiles():
    # SOMEDAY make less manual
    user_ids = []
    users = User.objects.all()
    print("630",users)
    for user in users:
        user_id = User.objects.get(username=user).id
        print("633 ", user, user_id)
        user_ids.append(user_id)
    print("230 ", user_ids)
    member_profiles = Member_profile.objects.all()
    for member_profile in member_profiles:
        print("638 ", member_profile)
        #member_id = Member_profile.objects.get(username=user).id
    #     print("233 ", user_ids.count(test_list))
    return

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
