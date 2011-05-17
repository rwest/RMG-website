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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect

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
    view prompts the user for the method by which they want to input data.
    """
    if request.method == 'POST':
        form = InputMethodForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method']
            if method == 'wizard':
                return HttpResponseRedirect('/measure/wizard')
            elif method == 'upload':
                return HttpResponseRedirect('/measure/upload')
            else:
                raise Http404('Invalid input method "{0}"; should be "wizard" or "upload".'.format(method))
    else:
        form = InputMethodForm()
    return render_to_response('start.html', {'form': form}, context_instance=RequestContext(request))
