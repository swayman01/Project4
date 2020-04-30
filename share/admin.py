from django.contrib import admin

# Register your models here.
from share.models import Member_profile

@admin.register(Member_profile) # @ decorator does exactly the same thing as the admin.site.register() syntax
class Member_profileAdmin(admin.ModelAdmin):
    pass
