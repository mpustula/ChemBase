# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:31:32 2017

@author: marcin
"""

from django import forms


class SearchForm(forms.Form):
    text=forms.CharField(label='Text to find',required=False)
