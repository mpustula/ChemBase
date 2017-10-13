from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from .models import Compound,Pictogram,GHSClass,Cmpd_Class,SystemLog

admin.site.register(Permission)
admin.site.register(Compound)
admin.site.register(Pictogram)
admin.site.register(GHSClass)
admin.site.register(Cmpd_Class)
admin.site.register(SystemLog)