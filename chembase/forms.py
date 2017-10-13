# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:31:32 2017

@author: marcin
"""

from django import forms
from django_select2.forms import (Select2Widget,ModelSelect2Widget,Select2MultipleWidget,ModelSelect2MultipleWidget,Select2TagWidget)
from .models import Group,Compound,GHSClass,Item

class SearchForm(forms.Form):
    text=forms.CharField(label='Text to find',required=False)
    cas=forms.CharField(label='CAS',required=False)
    place=forms.CharField(label='Place',required=False)
    smiles=forms.CharField(label='smiles',required=False)
    deleted=forms.BooleanField(required=False)
    cutoff=forms.DecimalField(widget=forms.NumberInput(attrs={'value':"0.6"}),min_value=0.00,max_value=1.00,decimal_places=2,required=False,initial=0.60)
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
        
        
class ItemForm(forms.ModelForm):
    
    class Meta:
        model=Item
        exclude=['compound']
        widgets={'group':ModelSelect2Widget(queryset=Group.objects.all(),
            search_fields=['group_name__icontains'])}
        
        
    

    
