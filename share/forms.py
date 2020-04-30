import datetime

from django import forms
from django.forms import ModelForm, Textarea, inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from share.models import Member_profile

# Add as needed
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _

# From https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
class Sign_upForm(UserCreationForm):
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email',required=False)
    # This approach did not work
    # fields = ['username','password','first_name','last_name','email']


class Member_profileForm(forms.Form):
    # model = Member_profile
    # fields = ['phone_number','city','state','zipcode','member_bio']
    phone_number = forms.CharField(label='Phone or Text Number',required=False)
    city = forms.CharField(label='City',required=False)
    state = forms.CharField(label='State Code (2 Letters)',required=True)
    zip_code =   forms.CharField(label='Zip Code',required=True)
    # ref: https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#built-in-widgets
    member_bio = forms.CharField(label='Tell us about yourself',widget=forms.Textarea)
    # print("32: city:", forms.CharField.cleaned_data['city']," state:",state," zip_code:",zip_code)

# reference: https://stackoverflow.com/questions/16719079/django-forms-custom-validation-on-two-fields-one-or-the-other
    # def clean(self):
    #     check = [self.cleaned_data['city'], self.cleaned_data['state'],self.cleaned_data['zip_code']]
    #     if any(check) and not all(check):
    #         # possible add some errors
    #         return self.cleaned_data
    #     raise ValidationError('Select any one')
