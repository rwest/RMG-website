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
This module defines the Django models used by the pdep app.
"""

import os
import os.path

from django.db import models

import rmgweb.settings as settings

from fields import *

################################################################################

class Network(models.Model):
    """
    A Django model of a pressure-dependent reaction network. 
    """
    def upload_input_to(instance, filename):
        # Always name the uploaded input file "input.py"
        return 'pdep/networks/{0}/input.py'.format(instance.pk)
    title = models.CharField(max_length=50)
    inputFile = models.FileField(upload_to=upload_input_to, verbose_name='Input file')
    inputText = models.TextField(blank=True, verbose_name='')

    def getDirname(self):
        """
        Return the absolute path of the directory that the Network object uses
        to store files.
        """
        return os.path.join(settings.MEDIA_ROOT, 'pdep', 'networks', str(self.pk))
    
    def getInputFilename(self):
        """
        Return the absolute path of the input file.
        """
        return os.path.join(self.getDirname(), 'input.py')
    
    def getOutputFilename(self):
        """
        Return the absolute path of the output file.
        """
        return os.path.join(self.getDirname(), 'output.py')
    
    def getLogFilename(self):
        """
        Return the absolute path of the log file.
        """
        return os.path.join(self.getDirname(), 'MEASURE.log')
    
    def getSurfaceFilenamePNG(self):
        """
        Return the absolute path of the PES image file in PNG format.
        """
        return os.path.join(self.getDirname(), 'PES.png')
    
    def getSurfaceFilenamePDF(self):
        """
        Return the absolute path of the PES image file in PDF format.
        """
        return os.path.join(self.getDirname(), 'PES.pdf')
    
    def getSurfaceFilenameSVG(self):
        """
        Return the absolute path of the PES image file in SVG format.
        """
        return os.path.join(self.getDirname(), 'PES.svg')
    
    def inputFileExists(self):
        """
        Return ``True`` if the input file exists on the server or ``False`` if
        not.
        """
        return os.path.exists(self.getInputFilename())
        
    def outputFileExists(self):
        """
        Return ``True`` if the output file exists on the server or ``False`` if
        not.
        """
        return os.path.exists(self.getOutputFilename())
        
    def logFileExists(self):
        """
        Return ``True`` if the log file exists on the server or ``False`` if
        not.
        """
        return os.path.exists(self.getLogFilename())
        
    def surfaceFilePNGExists(self):
        """
        Return ``True`` if a potential energy surface PNG image file exists or
        ``False`` if not.
        """
        return os.path.exists(self.getSurfaceFilenamePNG())
        
    def surfaceFilePDFExists(self):
        """
        Return ``True`` if a potential energy surface PDF image file exists or
        ``False`` if not.
        """
        return os.path.exists(self.getSurfaceFilenamePDF())
        
    def surfaceFileSVGExists(self):
        """
        Return ``True`` if a potential energy surface SVG image file exists or
        ``False`` if not.
        """
        return os.path.exists(self.getSurfaceFilenameSVG())
        
    def createDir(self):
        """
        Create the directory (and any other needed parent directories) that
        the Network uses for storing files.
        """
        try:
            os.makedirs(self.getDirname())
        except OSError:
            # Fail silently on any OS errors
            pass
        
    def deleteInputFile(self):
        """
        Delete the input file for this network from the server.
        """
        if self.inputFileExists():
            os.remove(self.getInputFilename())
        
    def deleteOutputFile(self):
        """
        Delete the output file for this network from the server.
        """
        if self.outputFileExists():
            os.remove(self.getOutputFilename())
        
    def deleteSurfaceFilePNG(self):
        """
        Delete the PES image file in PNF format for this network from the 
        server.
        """
        if os.path.exists(self.getSurfaceFilenamePNG()):
            os.remove(self.getSurfaceFilenamePNG())
        
    def deleteSurfaceFilePDF(self):
        """
        Delete the PES image file in PDF format for this network from the 
        server.
        """
        if os.path.exists(self.getSurfaceFilenamePDF()):
            os.remove(self.getSurfaceFilenamePDF())
        
    def deleteSurfaceFileSVG(self):
        """
        Delete the PES image file in SVG format for this network from the 
        server.
        """
        if os.path.exists(self.getSurfaceFilenameSVG()):
            os.remove(self.getSurfaceFilenameSVG())
        
    def loadInputText(self):
        """
        Load the input file text into the inputText field.
        """
        self.inputText = ''
        if self.inputFileExists():
            f = open(self.getInputFilename(),'r')
            for line in f:
                self.inputText += line
            f.close()
        
    def saveInputText(self):
        """
        Save the contents of the inputText field to the input file.
        """
        fpath = self.getInputFilename()
        self.createDir()
        f = open(fpath,'w')
        for line in self.inputText.splitlines():
            f.write(line + '\n')
        f.close()

################################################################################

class Species(models.Model):
    """
    A Django representation of a chemical species.
    """
    network = models.ForeignKey(Network)
    label = models.CharField(max_length=60)
    structure = models.CharField(max_length=200)
    E0 = QuantityField(form_class=EnergyField, verbose_name='Ground-state energy')
    
    def __unicode__(self):
        return self.label

################################################################################

class Reaction(models.Model):
    """
    A Django representation of a high-pressure-limit chemical reaction.
    """
    network = models.ForeignKey(Network)
    reactant1 = models.ForeignKey(Species, related_name='reactant1')
    reactant2 = models.ForeignKey(Species, related_name='reactant2', blank=True, null=True)
    product1 = models.ForeignKey(Species, related_name='product1')
    product2 = models.ForeignKey(Species, related_name='product2', blank=True, null=True)
    E0 = QuantityField(form_class=EnergyField, verbose_name='Transition-state energy')
