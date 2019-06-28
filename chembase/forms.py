# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:31:32 2017

@author: marcin
"""

from django import forms
from django_select2.forms import (Select2Widget,ModelSelect2Widget,Select2MultipleWidget,ModelSelect2MultipleWidget,Select2TagWidget)
from .models import Group,Compound,GHSClass,Item,OwnershipGroup, ExtraPermissions, UserProfile, ORZForm, CompoundForExperiments, ProteinTarget, ExperimentType, Experiment
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
    #ewid=forms.BooleanField(required=False)
    #resp=forms.BooleanField(required=False)
    paper_sds=forms.BooleanField(required=False)
    sds_file = forms.FileField(required=False)
    class_extr=forms.ModelMultipleChoiceField(widget=Select2MultipleWidget,queryset=GHSClass.objects.all(),required=False)
    class Meta:
        model=Compound
        #fields=['name','all_names','subtitle']
        exclude=['class_extr','image','author','group']
        widgets={'pictograms':Select2MultipleWidget,'sds':Select2Widget,'class_extr':Select2MultipleWidget,'storage_temp':Select2Widget}
        #'storage_temp':Select2Widget}
        
class GroupForm(forms.Form):
    group=forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=Group.objects.all(),
            search_fields=['group_name__icontains'],attrs={'data-tags':'true'}),queryset=Group.objects.all(),required=False)        
#        
#class GroupChoices(AutoModelSelect2TagField):
#        queryset = Group.objects
#        search_fields = ['group_name__icontains']
#    
#        def get_model_field_values(self, value):
#            return {'name': value }
            
            
class GHSClassForm(forms.Form):
    ghs_class=forms.ModelMultipleChoiceField(widget=ModelSelect2Widget(queryset=GHSClass.objects.all(),
            search_fields=['class_text__icontains']),queryset=GHSClass.objects.all(),required=False)
    number=forms.CharField(required=False)
    
class ItemForm(forms.ModelForm):
    room_choices=set([item.room for item in Item.objects.all()])
    comment=forms.CharField(required=False)
    ewid=forms.BooleanField(required=False)
    resp=forms.BooleanField(required=False)
    dailyused=forms.CharField(required=False)
    #group = forms.ModelChoiceField(widget=Select2TagWidget(attrs={'data-maximum-selection-length': 1,'data-placeholder':'Group','data-minimum-input-length':"0"}),queryset=Group.objects.all(),required=False)
    room=forms.ChoiceField(widget=Select2Widget(attrs={'data-tags':'true','required':'true'}),choices=((x,x) for x in room_choices))
    #place=forms.ChoiceField(widget=Select2Widget(attrs={'data-tags':'true'}),choices=((x,x) for x in room_choices))
    class Meta:
        model=Item
        exclude=['compound','room','group','storage_temp']
        widgets={'place':Select2Widget(attrs={'data-tags':'true','required':'true'}),
                 'place_num':Select2Widget(attrs={'data-tags':'true','required':'true'}),
                 'owner':Select2Widget}


class CompoundForExperimentsForm(forms.ModelForm):

    class Meta:
        model=CompoundForExperiments
        #fields=['name','all_names','subtitle']
        exclude=['image','author']

class ProteinTargetForm(forms.Form):
    target = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ProteinTarget.objects.all(),
                                                              search_fields=['target__icontains'],
                                                              attrs={'data-tags':'true'}),
                                    queryset=ProteinTarget.objects.all(), required=False)
    #class Meta:
    #    model = ProteinTarget
    #    exclude = ['target']
    #    widgets = {'target': Select2Widget(attrs={'data-tags': 'true', 'required': 'true'})}

class ExperimentTypeForm(forms.Form):
    exp_type = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ExperimentType.objects.all(),
                                                                search_fields=['exp_type__icontains'],
                                                                attrs={'data-tags':'true'}),
                                      queryset=ExperimentType.objects.all(),required=False)

    #class Meta:
    #    model = ExperimentType
    #    exclude = ['exp_type']
        #widgets = {'exp_type': Select2Widget(attrs={'data-tags': 'true', 'required': 'true'})}

class ExperimentForm(forms.ModelForm):
    unit_choices = ['mol', 'mmol', 'µmol', 'nmol', 'pmol']
    binding_unit = forms.ChoiceField(widget=Select2Widget(attrs={'data-tags':'true','required':'true'}),
                                     choices=((i*3, x) for i, x in enumerate(unit_choices)), initial=6)
    # target = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ProteinTarget.objects.all(),
    #                                                           search_fields=['target__icontains'],
    #                                                           attrs={'data-tags':'true'}),
    #                                 queryset=ProteinTarget.objects.all(), required=False)
    # exp_type = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ExperimentType.objects.all(),
    #                                                             search_fields=['exp_type__icontains'],
    #                                                             attrs={'data-tags':'true'}),
    #                                   queryset=ExperimentType.objects.all(),required=False)

    class Meta:
        model = Experiment
        fields = ['exp_details', 'active', 'binding_const', 'comment']
        #exclude = ['author', 'cmpd']
        #widgets = {'target': Select2Widget(attrs={'data-tags': 'true', 'required': 'true'}),
        #           'exp_type': Select2Widget(attrs={'data-tags': 'true', 'required': 'true'}),
        #           }


class ExperimentSearchForm(forms.Form):
    text = forms.CharField(required=False)

    cas = forms.CharField(label='CAS', required=False)
    exp_type = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ExperimentType.objects.all(),
                                                                search_fields=['exp_type__icontains'],
                                                                attrs={'data-tags': 'false'}),
                                      queryset=ExperimentType.objects.all(), required=False)
    target = forms.ModelChoiceField(widget=ModelSelect2Widget(queryset=ProteinTarget.objects.all(),
                                                              search_fields=['target__icontains'],
                                                              attrs={'data-tags':'false'}),
                                    queryset=ProteinTarget.objects.all(), required=False)

    smiles = forms.CharField(label='smiles', required=False)

    cutoff = forms.DecimalField(widget=forms.NumberInput(attrs={'value': "0.4"}), min_value=0.00, max_value=1.00,
                                decimal_places=2, required=False, initial=0.40)
    stype = forms.ChoiceField(widget=Select2Widget, choices=(('sim', 'Similarity'), ('sub', 'Substructure')),
                              required=False)

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
        
        
class ORZ_Form(forms.ModelForm):
    stanowisko=forms.CharField(required=False)
    kod_stanowiska=forms.CharField(required=False)
    
    class Meta:
        model=ORZForm
        fields=['owner','date_from','date_to']
        widgets={'owner':Select2Widget}
                                
                            
class ExpirePasswords(forms.Form):
    users=forms.ModelMultipleChoiceField(widget=ModelSelect2MultipleWidget(queryset=User.objects.all(),
            search_fields=['last_name__icontains']),queryset=User.objects.all(),required=False)
    exp_date=forms.IntegerField(required=True)
    if_mail=forms.BooleanField(required=False)


class OwnershipGroupForm(forms.ModelForm):

    class Meta:
        model = OwnershipGroup
        fields = {'name','short_name','admin'}
        widgets = {'admin': ModelSelect2Widget(queryset=User.objects.all(),
            search_fields=['last_name__icontains'])}


    
