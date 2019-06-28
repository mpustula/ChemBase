from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (Compound,Pictogram,GHSClass,Cmpd_Class,SystemLog,Item,
                    Annotation,Group,History,OwnershipGroup,UserProfile, 
                    ExtraPermissions, ORZForm, MailTemplates, ORZExtraFields,
                     CompoundForExperiments, Experiment, ProteinTarget, ExperimentType, ExperimentLog)

# Register your models here.
admin.site.register(Permission)
admin.site.register(OwnershipGroup)
admin.site.register(ExtraPermissions)
admin.site.register(Compound)
admin.site.register(Item)
admin.site.register(Pictogram)
admin.site.register(GHSClass)
admin.site.register(Cmpd_Class)
admin.site.register(SystemLog)
admin.site.register(Annotation)
admin.site.register(Group)
admin.site.register(History)
admin.site.register(ORZForm)
admin.site.register(ORZExtraFields)
admin.site.register(MailTemplates)
admin.site.register(CompoundForExperiments)
admin.site.register(Experiment)
admin.site.register(ProteinTarget)
admin.site.register(ExperimentType)
admin.site.register(ExperimentLog)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class OwnershipInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User profiles'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (OwnershipInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)