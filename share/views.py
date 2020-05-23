# References for querying
# https://docs.djangoproject.com/en/3.0/ref/models/querysets/#queryset-api
#  Try .values for python queries
# https://docs.djangoproject.com/en/3.0/ref/models/querysets/#field-lookups
#  Try .contains, .explain()


# Reference for editing/creating Provisions https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/
import json, os, operator, datetime, pytz
from datetime import date, datetime
# reference http://bradmontgomery.blogspot.com/2009/06/adding-q-objects-in-django.html
# and https://stackoverflow.com/questions/45253994/django-filter-with-or-statement
from django.db.models import Q
from django.urls import reverse, reverse_lazy #, path
# from django.views.generic.list import ListView
from django.views import generic
from django.views.generic import TemplateView, View
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

# from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth import login, logout, authenticate # 9/28/19 from django documentation and https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# from django.contrib.auth.forms import UserCreationForm # 9/28/19 from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

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
                member_bio = member_bio,
                name = username
            )
            member_profile_new.save()
            print("107 ready to send email", username)
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
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_name = user.username
    # member_id = Provision.member_id
    my_profile = Member_profile.objects.filter(member_id=user.id).first()
    if my_profile == None:
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
    provisionlast = Provision.objects.last()
    if int(Provision.objects.last().member_id)==0:
        create_provision(request)
    if int(Need.objects.last().member_id)==0:
        create_need(request)
    if my_profile.is_moderator == True:
        provisions = Provision.objects.all()
        needs = Need.objects.all()
    else:
        # provisions = list(Provision.objects.filter(member_id=user_id).
        # filter(Q(status='Available')|Q(status='Pending')|
        # Q(status='available')|Q(status='pending'))) #REMOVE 5/20/20
        provisions = Provision.objects.filter(member_id=user_id). \
        filter(Q(status='Available')|Q(status='Pending')| \
        Q(status='available')|Q(status='pending'))
        # provisions = Provision.objects.filter(member_id=user_id) # For Debugging
        for provision in provisions:
            provision.expiration_date = format_date(provision.expiration_date)
            # if provision.expiration_date!=None: #Commented out before 5/16/20
            #     provision.expiration_date = provision.expiration_date.strftime("%b %, %Y")
        # needs = list(Need.objects.filter(member_id=user_id).
        # filter(Q(status='Open')|Q(status='open')|Q(status='Pending'))) # Remove 5/21/20
        needs = Need.objects.filter(member_id=user_id). \
        filter(Q(status='Open')|Q(status='open')|Q(status='Pending')|Q(status='pending'))
        for need in needs:
            need.due_date = format_date(need.due_date)
    expiration_due_date_check(request,provisions,needs)
    #TODO repeate for status_update
    provisions_active = Provision.objects.filter(member_id=user_id).filter(Q(status='Pending')|Q(status='pending'))
    print("184: TODO If pending doesn't have provided_to, change to Available")
    provisions_activeLIST = []
    for provision in provisions_active:
        provided_to_name = User.objects.get(id=provision.provided_to).username
        provisionLIST = [provision.name,provided_to_name,provision.status,provision.id,provision.provided_to]
        provisions_activeLIST.append(provisionLIST)
        # print("188",provisions_activeLIST)

    needs_active = Need.objects.filter(member_id=user_id).filter(Q(status='Pending')|Q(status='pending'))
    print("184: TODO If pending doesn't have provided_to, change to Available")
    needs_activeLIST = []
    for need in needs_active:
        provided_from_name = User.objects.get(id=need.provided_from).username
        needLIST = [need.name,provided_from_name,need.status,need.id,need.provided_from]
        needs_activeLIST.append(needLIST)
        print("199",needs_activeLIST)

    context = {
    'user_is_authenticated':request.user.is_authenticated,
    'user_is_approved':my_profile.is_approved,
    'my_profile':my_profile,
    'provisions': provisions,
    'provisions_active': provisions_activeLIST,
    'needs_active': needs_activeLIST,
    'needs': needs,
    }
    print("210",context)
    return render(request, 'share/summary.html/',context)

def format_date(date_in):
    """This function returns date in the desired format"""
    if date_in!=None:
        date_out = date_in.strftime("%b %d, %Y")
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
    # Commented out 5/14/20
    # datetime_str = provisions[len(provisions)-1].expiration_date.strftime("%m/%d/%y")
    # datetime_object = datetime.strptime(datetime_str, "%m/%d/%y")
    # Provision.objects.filter(id=last_provision_id).update(expiration_date=datetime_object)
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
    # First filter needs by type
    # needs_filtered_by_typeLIST = list(Need.objects.filter(type=provision.type). \
    # filter(Q(status='Open')|Q(status='open')|Q(status='Pending')))
    # print("235",needs_filtered_by_typeLIST)
    needs = Need.objects.filter(type=provision.type).filter(~Q(member_id=member_id)). \
    filter(Q(status='Open')|Q(status='open')|Q(status='Pending')|Q(status='pending'))
    # print("230",needs_filtered_by_typeLIST,len(needs_filtered_by_typeLIST))
    needsLIST = []
    for need in needs:
        needSET = set(need.name.lower().split())
        common_words = provisionSET.intersection(needSET)
        # print("240",common_words)
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
        print("251",pk1,pk2)
        context = {
        'need': need,
        'error': 'has been retracted'
        }
        return render(request,'share/need_not_needed.html/',context)
    user = User.objects.filter(id=member_id)
    contact = Member_profile.objects.filter(member_id=member_id).first()
    provision = Provision.objects.filter(id=pk2).first()
    print("237", provision)
    provision.expiration_date = format_date(provision.expiration_date)
    context = {
    'provision':provision,
    'need': need,
    "contact":contact,
    "user":user,
    }
    print("241",context)
    return render(request, 'share/need_contact_info.html/',context)


@login_required
def provision_contact_info(request,pk1,pk2):
    provision = Provision.objects.get(id=pk1)
    member_id = Provision.objects.get(id=pk1).member_id
    print("315 provision,member_id",provision,member_id)
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
    print("328", need)
    need.due_date = format_date(need.due_date)
    context = {
    'provision':provision,
    'need': need,
    "contact":contact,
    "user":user,
    }
    print("336",context)
    return render(request, 'share/provision_contact_info.html/',context)


@login_required
# def need_not_needed(request,id1,id2):
def need_not_needed(request):
    print("263")
    print("263",id1,id2)
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
    print("357, pk1, pk2, pk3, pk4", pk1, pk2, pk3, pk4)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    my_profile = Member_profile.objects.filter(member_id=user.id).first()
    # if my_profile.is_moderator == True: #moved 5/19/20
    #     provisions = list(Provision.objects.all())
    #     needs = list(Need.objects.all())
    # else:
    #     provisions = list(Provision.objects.filter(member_id=user_id).
    #     filter(Q(status='Available')|Q(status='Pending')|
    #     Q(status='available')|Q(status='pending')))
    #     for provision in provisions:
    #         provision.expiration_date = format_date(provision.expiration_date)
    #
    #         # if provision.expiration_date!=None: #Commented out before 5/16/20
    #         #     provision.expiration_date = provision.expiration_date.strftime("%b %, %Y")
    #     needs = list(Need.objects.filter(member_id=user_id).
    #     filter(Q(status='Open')|Q(status='open')|Q(status='Pending')))
    #     for need in needs:
    #         need.due_date = format_date(need.due_date)
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
        print("392 need update")
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

            # if provision.expiration_date!=None: #Commented out before 5/16/20
            #     provision.expiration_date = provision.expiration_date.strftime("%b %, %Y")
        # needs = list(Need.objects.filter(member_id=user_id).
        # filter(Q(status='Open')|Q(status='open')|Q(status='Pending')))
        needs = Need.objects.filter(member_id=user_id). \
        filter(Q(status='Open')|Q(status='open')|Q(status='Pending'))
        for need in needs:
            need.due_date = format_date(need.due_date)
    provisions = Provision.objects.filter(member_id=user_id)  \
    .filter(Q(status='Available')|Q(status='Pending'))
    needs = Need.objects.filter(member_id=user_id) \
    .filter(Q(status='Open')|Q(status='open')|Q(status='Pending'))
    context = {
        'user_is_authenticated':request.user.is_authenticated,
        'user_is_approved':my_profile.is_approved,
        'my_profile':my_profile,
        'provisions': provisions,
        'needs': needs,
        }

    # summary(request) # This line did not eliminate the need for regenerating the context
    # return redirect('share/summary.html/',context) doesn't work 5/23/20
    # return render(request, summary) doesn't work 5/23/20
    return render(request, 'share/summary.html/',context)


@login_required
def expiration_due_date_check(request,provisions_queryset,needs_queryset):
    # print("376",request,provisions_queryset,needs_queryset)
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
                print("394 updated status",item,current_time,item.expiration_date,item.status)

        for item in needs_queryset:
            if item.due_date!=None:
                if current_time.replace(tzinfo=utc) > item.due_date.replace(tzinfo=utc):
                    item.status = 'Expired'
                    item.save()
                    print("401 updated status",item,current_time,item.due_date,item.status)
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
    fields = ['name', 'type', 'due_date','background_info']
    success_url = reverse_lazy('summary')


class NeedUpdate(UpdateView):
    model = Need
    fields = ['name', 'type', 'due_date','background_info','provided_from']
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
