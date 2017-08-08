# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:31:32 2017

@author: marcin
"""

from django import forms
from django_select2.forms import (Select2Widget)

class SearchForm(forms.Form):
    text=forms.CharField(label='Text to find',required=False)
    smiles=forms.CharField(label='smiles',required=False)
    deleted=forms.BooleanField(required=False)
    cutoff=forms.DecimalField(min_value=0,max_value=1,required=False)
    stype=forms.ChoiceField(widget=Select2Widget, choices=(('sim','Similarity'),('sub','Substructure')),required=False)
    
