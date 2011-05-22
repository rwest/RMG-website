#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
#	RMG Website - A Django-powered website for Reaction Mechanism Generator
#
#	Copyright (c) 2011 Prof. William H. Green (whgreen@mit.edu) and the
#	RMG Team (rmg_dev@mit.edu)
#
#	Permission is hereby granted, free of charge, to any person obtaining a
#	copy of this software and associated documentation files (the 'Software'),
#	to deal in the Software without restriction, including without limitation
#	the rights to use, copy, modify, merge, publish, distribute, sublicense,
#	and/or sell copies of the Software, and to permit persons to whom the
#	Software is furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in
#	all copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#	DEALINGS IN THE SOFTWARE.
#
################################################################################

"""
This module defines the Django forms used by the pdep app.
"""

from django import forms
from django.forms.models import inlineformset_factory

from models import *

################################################################################

class EditNetworkForm(forms.ModelForm):
    """
    A Django form for editing a MEASURE input file.
    """
    class Meta:
        model = Network
        fields = ('inputText',)

################################################################################

class UploadNetworkForm(forms.ModelForm):
    """
    A Django form for uploading a MEASURE input file.
    """
    class Meta:
        model = Network
        fields = ('inputFile',)
    
################################################################################

class SpeciesForm(forms.ModelForm):
    """
    A Django form for inputting attributes for a chemical species. This form is 
    based on the Species model.
    """
    class Meta:
        model = Species
    
SpeciesFormSet = inlineformset_factory(Network, Species, form=SpeciesForm, can_delete=False, extra=10)
