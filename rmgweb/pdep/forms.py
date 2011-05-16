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
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory

from models import *
from fields import *

################################################################################

class CollisionModelForm(forms.ModelForm):
    """
    A Django form for inputting parameters for a collision model. This form is 
    based on the CollisionModel model.
    """
    sigmaLJ = LJSigmaField(label=mark_safe('Lennard-Jones <span class="math">\sigma_\mathrm{LJ}</span>'))
    epsilonLJ = LJEpsilonField(label=mark_safe('Lennard-Jones <span class="math">\epsilon_\mathrm{LJ}</span>'))
    class Meta:
        model = CollisionModel
        
CollisionModelFormSet = inlineformset_factory(Species, CollisionModel, form=CollisionModelForm, can_delete=False, extra=1)

################################################################################

class SpeciesForm(forms.ModelForm):
    """
    A Django form for inputting attributes for a chemical species. This form is 
    based on the Species model.
    """
    class Meta:
        model = Species
    
    def __init__(self, *args, **kwargs):
        super(SpeciesForm, self).__init__(*args, **kwargs)
        kwargs.pop('auto_id'); kwargs.pop('empty_permitted') # kwargs that formsets can't handle
        self.collisionModelFormSet = CollisionModelFormSet(*args, **kwargs)
        
    def clean_structure(self):
        """
        Custom validation for the structure field to ensure that a valid
        representation of the structure has been provided. Currently this is
        limited to either InChI or SMILES.
        """
        from rmgpy.chem.molecule import Molecule
        
        structure = str(self.cleaned_data['structure'])
        try:
            molecule = Molecule()
            if structure[0:6] == 'InChI=':
                molecule.fromInChI(structure)
            else:
                molecule.fromSMILES(structure)
        except Exception, e:
            raise forms.ValidationError('Invalid value.')
        return structure
