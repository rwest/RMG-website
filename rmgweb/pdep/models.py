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

from django.db import models

from fields import *

################################################################################

class Species(models.Model):
    """
    A Django representation of a chemical species.
    """
    label = models.CharField(max_length=60)
    structure = models.CharField(max_length=200)
    E0 = QuantityField(form_class=EnergyField, verbose_name='Ground-state energy')
    
    def __unicode__(self):
        return self.label

################################################################################

class CollisionModel(models.Model):
    """
    A Django representation of a set of collsion parameters with units. Each
    collision model is associated with exactly one species (and vice versa),
    so we represent this relationship with a OneToOneField.
    """
    species = models.OneToOneField(Species)
    molWt = QuantityField(form_class=MolecularWeightField, verbose_name='Molecular weight')
    sigmaLJ = QuantityField(form_class=LJSigmaField, verbose_name='Lennard-Jones sigma')
    epsilonLJ = QuantityField(form_class=LJEpsilonField, verbose_name='Lennard-Jones epsilon')
    
################################################################################

class States(models.Model):
    """
    A Django representation of a set of molecular degrees of freedom data.
    """
    pass
    
################################################################################

class Translation(models.Model):
    """
    A Django representation of 3D translational degrees of freedom using an
    infinite square well in the classical limit. Each translator is associated
    with a States object; we represent this using a ForeignKey.
    """
    states = models.ForeignKey(States)
    mass = models.FloatField(max_length=30)
    
################################################################################

class RigidRotor(models.Model):
    """
    A Django representation of an 2D (linear) or 3D (nonlinear) external rigid 
    rotor. For a linear rotor, only the inertiaA field is used; for a nonlinear 
    rotor, all three inertia fields are used. Each rigid rotor is associated
    with a States object; we represent this using a ForeignKey.
    """
    states = models.ForeignKey(States)
    linear = models.BooleanField()
    inertiaA = models.FloatField(max_length=30)
    inertiaB = models.FloatField(max_length=30)
    inertiaC = models.FloatField(max_length=30)
    inertia_units = models.CharField(max_length=30)
    symmetry = models.FloatField(max_length=30)
    
################################################################################

class HarmonicOscillator(models.Model):
    """
    A Django representation of a 1D harmonic oscillator. Each oscillator is 
    associated with a States object; we represent this using a ForeignKey.
    """
    states = models.ForeignKey(States)
    frequency = models.FloatField(max_length=30)
    frequency_units = models.CharField(max_length=30)
    
################################################################################

class HinderedRotor(models.Model):
    """
    A Django representation of a 1D Pitzer-Gwynn hindered rotor. This hindered
    rotor model is based on the simple cosine potential, and is defined by
    a reduced moment of inertia and a barrier height. Each hindered rotor is 
    associated with a States object; we represent this using a ForeignKey.
    """
    states = models.ForeignKey(States)
    inertia = models.FloatField(max_length=30)
    inertia_units = models.CharField(max_length=30)
    barrier = models.FloatField(max_length=30)
    barrier_units = models.CharField(max_length=30)
    symmetry = models.FloatField(max_length=30)
