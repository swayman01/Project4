from django.contrib import admin

# Register your models here.
from share.models import Member_profile, Provision, Need, Action_item

@admin.register(Member_profile) # @ decorator does exactly the same thing as the admin.site.register() syntax
class Member_profileAdmin(admin.ModelAdmin):
    pass

@admin.register(Provision) # @ decorator does exactly the same thing as the admin.site.register() syntax
class ProvisionAdmin(admin.ModelAdmin):
    pass

@admin.register(Need) # @ decorator does exactly the same thing as the admin.site.register() syntax
class NeedAdmin(admin.ModelAdmin):
    pass

@admin.register(Action_item) # @ decorator does exactly the same thing as the admin.site.register() syntax
class Action_itemAdmin(admin.ModelAdmin):
    pass
