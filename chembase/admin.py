from django.contrib import admin

# Register your models here.
from .models import Compound,Pictogram,GHSClass,Cmpd_Class


admin.site.register(Compound)
admin.site.register(Pictogram)
admin.site.register(GHSClass)
admin.site.register(Cmpd_Class)