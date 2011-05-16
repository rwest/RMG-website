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

from django import forms

from widgets import *

################################################################################

class NumberUnitsField(forms.MultiValueField):
    """
    A field for specifying a numeric value with corresponding units. Use the
    `choices` parameter in the constructor to specify the allowed units.
    """
    
    def __init__(self, choices, *args, **kwargs):
        fields = (
            forms.FloatField(),
            forms.ChoiceField(choices=choices),
        )
        kwargs['widget'] = InputAndChoiceWidget(choices)
        super(NumberUnitsField, self).__init__(fields, **kwargs)
        
    def compress(self, data_list):
        if data_list:
            try:
                value = float(data_list[0])
                units = str(data_list[1])
            except ValueError:
                raise forms.ValidationError('A numeric value is required.')
            return (value, units)
        return None

################################################################################

class EnergyField(NumberUnitsField):
    """
    A field for specifying an energy value with corresponding units.
    """
    
    def __init__(self, *args, **kwargs):
        choices = (
            ('J/mol', 'J/mol'),
            ('kJ/mol', 'kJ/mol'),
            ('cal/mol', 'cal/mol'),
            ('kcal/mol', 'kcal/mol'),
            ('cm^-1', 'cm^-1'),
        )
        super(EnergyField, self).__init__(choices, *args, **kwargs)

################################################################################

class MolecularWeightField(NumberUnitsField):
    """
    A field for specifying a molecular weight value with corresponding units.
    """
    
    def __init__(self, *args, **kwargs):
        choices = (
            ('u', 'u'),
            ('g/mol', 'g/mol'),
            ('kg/mol', 'kg/mol'),
            ('g/kmol', 'g/kmol'),
            ('kg/kmol', 'kg/kmol'),
        )
        super(MolecularWeightField, self).__init__(choices, *args, **kwargs)

################################################################################

class LJSigmaField(NumberUnitsField):
    """
    A field for specifying a Lennard-Jones sigma value with corresponding 
    units.
    """
    
    def __init__(self, *args, **kwargs):
        choices = (
            ('angstrom', 'angstrom'),
            ('m', 'm'),
        )
        super(LJSigmaField, self).__init__(choices, *args, **kwargs)

################################################################################

class LJEpsilonField(NumberUnitsField):
    """
    A field for specifying a Lennard-Jones epsilon value with corresponding 
    units.
    """
    
    def __init__(self, *args, **kwargs):
        choices = (
            ('K', 'K'),
            ('J/mol', 'J/mol'),
            ('kJ/mol', 'kJ/mol'),
            ('cal/mol', 'cal/mol'),
            ('kcal/mol', 'kcal/mol'),
            ('cm^-1', 'cm^-1'),
        )
        super(LJEpsilonField, self).__init__(choices, *args, **kwargs)
