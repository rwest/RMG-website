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

import os.path
import time

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import *
from forms import *

################################################################################

def index(request):
    """
    The MEASURE homepage.
    """
    return render_to_response('measure.html', context_instance=RequestContext(request))

def start(request):
    """
    A view called when a user wants to begin a new MEASURE calculation. This
    view creates a new Network and redirects the user to the main page for that
    network.
    """
    # Create and save a new Network
    network = Network(title='Untitled Network')
    network.save()
    return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))

def networkIndex(request, networkKey):
    """
    A view called when a user wants to see the main page for a Network object
    indicated by `networkKey`.
    """
    network = get_object_or_404(Network, pk=networkKey)
    
    # Get file sizes of files in 
    filesize = {}; modificationTime = {}
    if network.inputFileExists():
        filesize['inputFile'] = '{0:.1f}'.format(os.path.getsize(network.getInputFilename()))
        modificationTime['inputFile'] = time.ctime(os.path.getmtime(network.getInputFilename()))
    if network.outputFileExists():
        filesize['outputFile'] = '{0:.1f}'.format(os.path.getsize(network.getOutputFilename()))
        modificationTime['outputFile'] = time.ctime(os.path.getmtime(network.getOutputFilename()))
    if network.logFileExists():
        filesize['logFile'] = '{0:.1f}'.format(os.path.getsize(network.getLogFilename()))
        modificationTime['logFile'] = time.ctime(os.path.getmtime(network.getLogFilename()))
    if network.surfaceFilePNGExists():
        filesize['surfaceFilePNG'] = '{0:.1f}'.format(os.path.getsize(network.getSurfaceFilenamePNG()))
        modificationTime['surfaceFilePNG'] = time.ctime(os.path.getmtime(network.getSurfaceFilenamePNG()))
    if network.surfaceFilePDFExists():
        filesize['surfaceFilePDF'] = '{0:.1f}'.format(os.path.getsize(network.getSurfaceFilenamePDF()))
        modificationTime['surfaceFilePDF'] = time.ctime(os.path.getmtime(network.getSurfaceFilenamePDF()))
    if network.surfaceFileSVGExists():
        filesize['surfaceFileSVG'] = '{0:.1f}'.format(os.path.getsize(network.getSurfaceFilenameSVG()))
        modificationTime['surfaceFileSVG'] = time.ctime(os.path.getmtime(network.getSurfaceFilenameSVG()))
        
    return render_to_response('networkIndex.html', {'network': network, 'networkKey': networkKey, 'filesize': filesize, 'modificationTime': modificationTime}, context_instance=RequestContext(request))

def networkWizard(request, networkKey):
    """
    A view called when a user wants to add/edit Network input parameters using
    the wizard.
    """
    return HttpResponseRedirect(reverse(networkWizardSpecies,args=(networkKey,)))

def networkWizardSpecies(request, networkKey):
    """
    The first view in the input wizard, involving adding of species to the
    network.
    """
    network = get_object_or_404(Network, pk=networkKey)
    if request.method == 'POST':
        if 'add_species' in request.POST:
            post = request.POST.copy()
            post['species_set-TOTAL_FORMS'] = int(post['species_set-TOTAL_FORMS']) + 5
            formset = SpeciesFormSet(post, instance=network)
            # The above will still attempt to validate the form, so suppress the errors it generates
            for form in formset: form._errors = {}
        else:
            formset = SpeciesFormSet(request.POST, instance=network)
            if formset.is_valid():
                # Save the formset
                formset.save()
                # Go to next step
                return HttpResponseRedirect(reverse(networkWizardReactions,args=(network.pk,)))
    else:
        # Create the form
        formset = SpeciesFormSet(instance=network)
    return render_to_response('networkWizardSpecies.html', {'network': network, 'networkKey': networkKey, 'formset': formset}, context_instance=RequestContext(request))

def networkWizardReactions(request, networkKey):
    """
    The second view in the input wizard, involving adding of reactions to the
    network.
    """
    network = get_object_or_404(Network, pk=networkKey)
    if request.method == 'POST':
        if 'add_reactions' in request.POST:
            post = request.POST.copy()
            post['reaction_set-TOTAL_FORMS'] = int(post['reaction_set-TOTAL_FORMS']) + 5
            formset = ReactionFormSet(post, instance=network)
            # The above will still attempt to validate the form, so suppress the errors it generates
            for form in formset: form._errors = {}
        else:
            formset = ReactionFormSet(request.POST, instance=network)
            if formset.is_valid():
                # Save the formset
                formset.save()
                # Go to next step
                return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))
    else:
        # Create the form
        formset = ReactionFormSet(instance=network)
    return render_to_response('networkWizardReactions.html', {'network': network, 'networkKey': networkKey, 'formset': formset}, context_instance=RequestContext(request))

def networkEditor(request, networkKey):
    """
    A view called when a user wants to add/edit Network input parameters by
    editing the input file in the broswer
    """
    network = get_object_or_404(Network, pk=networkKey)
    if request.method == 'POST':
        form = EditNetworkForm(request.POST, instance=network)
        if form.is_valid():
            # Save the inputText field contents to the input file
            network.saveInputText()
            # Save the form
            network = form.save()
            # Go back to the network's main page
            return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))
    else:
        # Load the text from the input file into the inputText field
        network.loadInputText()
        # Create the form
        form = EditNetworkForm(instance=network)
    return render_to_response('networkEditor.html', {'network': network, 'networkKey': networkKey, 'form': form}, context_instance=RequestContext(request))

def networkUpload(request, networkKey):
    """
    A view called when a user wants to add/edit Network input parameters by
    uploading an input file.
    """
    network = get_object_or_404(Network, pk=networkKey)
    if request.method == 'POST':
        form = UploadNetworkForm(request.POST, request.FILES, instance=network)
        if form.is_valid():
            # Delete the current input file
            network.deleteInputFile()
            # Save the form
            network = form.save()
            # Load the text from the input file into the inputText field
            network.loadInputText()
            # Go back to the network's main page
            return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))
    else:
        # Create the form
        form = UploadNetworkForm(instance=network)
    return render_to_response('networkUpload.html', {'network': network, 'networkKey': networkKey, 'form': form}, context_instance=RequestContext(request))

def networkDrawPNG(request, networkKey):
    """
    A view called when a user wants to draw the potential energy surface for
    a given Network in PNG format.
    """
    from rmgpy.measure.main import execute
    
    network = get_object_or_404(Network, pk=networkKey)
    
    # Run MEASURE to draw the PES
    execute(
        inputFile = network.getInputFilename(),
        drawFile = network.getSurfaceFilenamePNG(),
    )
    
    # Go back to the network's main page
    return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))

def networkDrawPDF(request, networkKey):
    """
    A view called when a user wants to draw the potential energy surface for
    a given Network in PDF format.
    """
    from rmgpy.measure.main import execute
    
    network = get_object_or_404(Network, pk=networkKey)
    
    # Run MEASURE to draw the PES
    execute(
        inputFile = network.getInputFilename(),
        drawFile = network.getSurfaceFilenamePDF(),
    )
    
    # Go back to the network's main page
    return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))

def networkDrawSVG(request, networkKey):
    """
    A view called when a user wants to draw the potential energy surface for
    a given Network in SVG format.
    """
    from rmgpy.measure.main import execute
    
    network = get_object_or_404(Network, pk=networkKey)
    
    # Run MEASURE to draw the PES
    # For some reason SVG drawing seems to be much slower than the other formats
    execute(
        inputFile = network.getInputFilename(),
        drawFile = network.getSurfaceFilenameSVG(),
    )
    
    # Go back to the network's main page
    return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))

def networkRun(request, networkKey):
    """
    A view called when a user wants to run MEASURE on the input file for a
    given Network.
    """
    from rmgpy.measure.main import execute
    
    network = get_object_or_404(Network, pk=networkKey)
    
    # Run MEASURE! This may take some time...
    execute(
        inputFile = network.getInputFilename(),
        outputFile = network.getOutputFilename(),
    )
    
    # Go back to the network's main page
    return HttpResponseRedirect(reverse(networkIndex,args=(network.pk,)))
