from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from datetime import date
#import uuid # Required for unique instances
# another reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

#https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
class Member_profile(models.Model):
    """
        Model contains supplemental data that is not part of the
        django.contrib.auth.models User Model


Phone/Text # (optional)
City/State/Zip
Member Bio
        """

    is_approved = models.BooleanField(default=False,
    help_text='True means Administrator has allowed member to join')
    phone_number = models.CharField(max_length=15, blank=True,
    help_text='Optional, used for making contact outside of app')
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True,
    help_text="Use standard 2-character codes")
    zip_code = models.CharField(max_length=15, blank=True)
    member_bio = models.TextField(max_length=1000, blank=False)
    member_id = models.PositiveSmallIntegerField(blank=False)

    # TODO: Decide if we need this
    def get_absolute_url(self):
        # Returns the url to access a particular pizza instance.
        return reverse('memberprofile_detail', args=[str(self.id)])

    # def __str__(self): #Commented out 4/25/20
    #     # String for representing the Model object.
    #     return self.name

# built-in user model:
#  username
#  password
#  check Password
#  first_name
#  last_name
#  email
#
#    last_login
#    date_joined
#  useful methods:
#    get_username()¶
#     Returns the username for the user. Since the User model can be swapped out,
#     you should use this method instead of referencing the username attribute directly.
#
# get_full_name()¶
#     Returns the first_name plus the last_name, with a space in between.
#
# get_short_name()¶
#     Returns the first_name.
#
# set_password(raw_password)¶
#     Sets the user’s password to the given raw string, taking care of the
#     password hashing. Doesn’t save the User object.
#
#  class models.UserManager¶
#     The User model has a custom manager that has the following helper methods
#     (in addition to the methods provided by BaseUserManager):
#
#     create_user(username, email=None, password=None, **extra_fields)¶
#         Creates, saves and returns a User.
#         The username and password are set as given. The domain portion of email
#         is automatically converted to lowercase, and the returned User object will have is_active set to True.
#         If no password is provided, set_unusable_password() will be called.
#         The extra_fields keyword arguments are passed through to the
#         User’s __init__ method to allow setting arbitrary fields on a custom user model.
#         See Creating users for example usage. https://docs.djangoproject.com/en/3.0/topics/auth/default/#topics-auth-creating-users
#
#
# member_profile:
#   user_id
#   phone_number (optional)
#   location:
#    city, state, zip code
#  approved (by administrator)
#
