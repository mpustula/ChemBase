# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:31:32 2017

@author: marcin
"""

from django import forms
from django_select2.forms import (Select2Widget,ModelSelect2Widget,Select2MultipleWidget,ModelSelect2MultipleWidget,Select2TagWidget)
from .models import Group,Compound,GHSClass,Item,OwnershipGroup, ExtraPermissions, UserProfile
from django.contrib.auth.models import User, Permission

class SearchForm(forms.Form):
    text=forms.CharField(label='Text to find',required=False)
    cas=forms.CharField(label='CAS',required=False)
    place=forms.CharField(label='Place',required=False)
    smiles=forms.CharField(label='smiles',required=False)
    deleted=forms.BooleanField(required=False)
    cutoff=forms.DecimalField(widget=forms.NumberInput(attrs={'value':"0.4"}),min_value=0.00,max_value=1.00,decimal_places=2,required=False,initial=0.40)
    stype=forms.ChoiceField(widget=Select2Widget, choices=(('sim','Similarity'),('sub','Substructure')),required=False)
    group=forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=Group.objects.all(),
            search_fields=['group_name__icontains']),queryset=Group.objects.all(),required=False)
            
            
class CompoundForm(forms.ModelForm):
    ewid=forms.BooleanField(required=False)
    sds_file = forms.FileField(required=False)
    class_extr=forms.ModelMultipleChoiceField(widget=Select2MultipleWidget,queryset=GHSClass.objects.all(),required=False)
    class Meta:
        model=Compound
        #fields=['name','all_names','subtitle']
        exclude=['class_extr','image','author']
        widgets={'pictograms':Select2MultipleWidget,'sds':Select2Widget,'class_extr':Select2MultipleWidget}
        
        
#        
#class GroupChoices(AutoModelSelect2TagField):
#        queryset = Group.objects
#        search_fields = ['group_name__icontains']
#    
#        def get_model_field_values(self, value):
#            return {'name': value }
        
class ItemForm(forms.ModelForm):
    room_choices=set([item.room for item in Item.objects.all()])
    comment=forms.CharField(required=False)
    #group = forms.ModelChoiceField(widget=Select2TagWidget(attrs={'data-maximum-selection-length': 1,'data-placeholder':'Group','data-minimum-input-length':"0"}),queryset=Group.objects.all(),required=False)
    room=forms.ChoiceField(widget=Select2Widget(attrs={'data-tags':'true','required':'true'}),choices=((x,x) for x in room_choices))
    #place=forms.ChoiceField(widget=Select2Widget(attrs={'data-tags':'true'}),choices=((x,x) for x in room_choices))
    class Meta:
        model=Item
        exclude=['compound','room']
        widgets={'group':Select2Widget(attrs={'data-tags':'true'}),
                 'place':Select2Widget(attrs={'data-tags':'true','required':'true'}),
                 'place_num':Select2Widget(attrs={'data-tags':'true','required':'true'}),
                 'owner':Select2Widget}
                 
                 
class UserForm(forms.ModelForm):
    password = forms.CharField(required=False,widget=forms.PasswordInput)
    password_commit = forms.CharField(required=False,widget=forms.PasswordInput)
    class Meta:
        model=User
        exclude=['password','date_joined','last_login']
        widgets={'groups':Select2MultipleWidget,'user_permissions':Select2MultipleWidget}
                
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model=UserProfile
        exclude=['user']
        widgets={'own_groups':Select2MultipleWidget}

class ExtraPermForm(forms.ModelForm):

    class Meta:
        model=ExtraPermissions
        exclude=['user']
        widgets={'group':Select2Widget,'permission':Select2Widget}       
                                
        
        
    

    
