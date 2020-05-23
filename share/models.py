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
        """
    name = models.CharField(max_length=50, help_text='')
    # title = models.CharField(max_length=50, blank=True) #commented out 5/6/20
    is_approved = models.BooleanField(default=False,
    help_text='True means Administrator has allowed member to join')
    is_moderator = models.BooleanField(default=False,
    help_text='Moderators can view and edit all Provisions and Needs')
    phone_number = models.CharField(max_length=15, blank=True,
    help_text='Optional, used for making contact outside of app')
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True,
    help_text="Use standard 2-character codes")
    zip_code = models.CharField(max_length=15, blank=True)
    member_bio = models.TextField(max_length=1000, blank=False)
    member_id = models.PositiveSmallIntegerField(blank=False)

    # TODO: Decide if we need this -trial comment out 5/12/20
    # def get_absolute_url(self):
    #     # Returns the url to access a particular pizza instance.
    #     return reverse('memberprofile_detail', args=[str(self.id)])

    def __str__(self):
         # String for representing the Model object.
         return self.name

# Make type global since it is used in two models
TYPE = (
('Service', 'Service'),
('Perishable Food', 'Perishable Food'),
('Non Perishable Food', 'Non Perishable Food'),
('Product', 'Product'),
('Financial', 'Financial'),
('Other', 'Other'),
)


class Provision(models.Model):
    """Model contains what the members can provide"""
    STATUS = (
    ('Available', 'Available'),
    ('Pending', 'Pending'),
    ('Provided', 'Provided'),
    ('Expired', 'Expired'),
    ('Retracted', 'Retracted'),
    )
    # Note - not allow people to reserve ahead of time
    FREQUENCY = (
    ('One Time', 'One_time'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Intermittent', 'Intermittent'),
    ('Not Applicable', 'Not Applicable'),
    )
    name = models.CharField(max_length=50, help_text='')
    member_id = models.PositiveSmallIntegerField(blank=False,
    help_text='Providing member',default=0)
    type = models.CharField(max_length=25, choices=TYPE)
    frequency = models.CharField(max_length=25, choices=FREQUENCY, default='One_time',
    help_text='Used for items that repeat (i.e. at service that can be provided \
    to one person every week')
    expiration_date = models.DateTimeField(auto_now=False, auto_now_add=False, \
    blank=True, null=True, help_text=('useful for food and deadlines'))
    status = models.CharField(max_length=25, choices=STATUS, default='Available')
    provided_to = models.PositiveSmallIntegerField(blank=True, null=True,
    help_text="Member who received the service")

    # class Meta:
    #     ordering = ['type', 'expiration_date'] # descending date in views.py?
        # there is another approach: https://github.com/carltongibson/django-filter/issues/274


    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('provision_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Need(models.Model):
    """Model contains what the members need"""
    STATUS = (
    ('Open', 'Open'),
    ('Pending', 'Pending'),
    ('Provided', 'Provided'),
    ('Expired', 'Expired'),
    ('Retracted', 'Retracted'),
    )
    name = models.CharField(max_length=50, help_text='')
    member_id = models.PositiveSmallIntegerField(blank=False,
    help_text='Member with need',default=0)
    type = models.CharField(max_length=25, choices=TYPE)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False, \
    blank=True, null=True, help_text='when is the item needed?')
    background_info = models.TextField(max_length=1000, blank=True, \
    help_text="Any additional information that might help")
    status = models.CharField(max_length=25, choices=STATUS, default='Open')
    provided_from = models.PositiveSmallIntegerField(blank=True, null=True,
    help_text="Member who provided the service")


    def get_absolute_url(self):
        """Returns the url to access a particular instance."""
        return reverse('provision_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name

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
