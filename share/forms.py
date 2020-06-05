import datetime, re

from django import forms
from django.forms import ModelForm, Textarea, inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.views.generic.edit import UpdateView
from django.shortcuts import render,redirect
from share.models import Member_profile
#from share.views import phone_number_checker

# Add as needed
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
def phone_number_checker(phone_number):
    """Simple phone number checker and formatter. Checks for 10 digits and uses
    dot format"""
    print("forms 17: phone_number_checker",phone_number)
    tel = re.compile('[0-9]')
    x = tel.findall(str(phone_number))
    if len(x)!=10:
        return (False,"telephone number must contain 10 digits")
    else:
        area_code = ""
        for i in range(0,3,1):
            area_code = area_code+x[i]
        exchange = "."
        for i in range(3,6,1):
            exchange = exchange + x[i]
        subscriber = "."
        for i in range(6,10,1):
            subscriber = subscriber + x[i]
        tel_no = area_code + exchange +subscriber
        return(True,tel_no)
# From https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
class Sign_upForm(UserCreationForm):
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email',required=True) # needed for password reset
    # This approach did not work
    # fields = ['username','password','first_name','last_name','email']


class Member_profileForm(forms.Form):
    phone_number = forms.CharField(label='Phone or Text Number',required=False)
    city = forms.CharField(label='City',required=False)
    state = forms.CharField(label='State Code (2 Letters)',required=True)
    zip_code =   forms.CharField(label='Zip Code',required=True)
    # ref: https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#built-in-widgets
    member_bio = forms.CharField(label='Tell us about yourself',widget=forms.Textarea)
    # print("32: city:", forms.CharField.cleaned_data['city']," state:",state," zip_code:",zip_code)
    # if phone_number != "":
    #     phone_number = phone_number_checker(phone_number)[1]
# reference: https://docs.djangoproject.com/en/2.2/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        print("forms 57 in def clean(self)")
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        print("forms 59",phone_number)
        if phone_number != "" and not phone_number_checker(phone_number)[0]:
            print("forms 61",phone_number_checker(phone_number))
            msg = "Phone number must contain exactly 10 digits"
            self.add_error('phone_number', msg)
            raise forms.ValidationError(msg)
            context = {
                'error':Member_profileForm().errors.as_data(),
                'error':Member_profileForm().errors.as_json(),
            }
        else:
            print("forms 86:caught by phone_number_checker")
            phone_number = phone_number_checker(phone_number)[1]
            return self.cleaned_data
