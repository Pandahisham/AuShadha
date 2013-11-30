################################################################################
# Project: AuShadha
# Description: Pane of the UI
# Author ; Dr.Easwar T.R
# Date: 04-11-2013
# License: GNU-GPL Version3, see LICENSE.txt for details
################################################################################

# General Django Imports----------------------------------
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.template import Template, Context
from cStringIO import StringIO
import yaml
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from patient import MODULE_LABEL
#from patient.models import PatientDetail

import importlib
from AuShadha.apps.ui.ui import ui as UI
patient = UI.registry.get('PatientRegistration','')
if patient:
  print "UI has PatientRegistration role and class defined"
  module = importlib.import_module(patient.__module__)
  PatientDetail = getattr(module, patient.__name__)
else:
  raise Exception("""
                  PatientRegistration role not defined and hence cannot be imported.
                  This module depends on this. 
                  Please register the module and class for PatientRegistration Role
                  """
                  )


@login_required
def render_medical_history_pane(request, patient_id = None):
  
  user = request.user
  
  if request.method == 'GET' and request.is_ajax():

    try:

      if patient_id:
        patient_id = int(patient_id)
      else:
        patient_id = int( request.GET.get('patient_id') )

      app_wrapper = []
      patient_detail_obj = PatientDetail.objects.get(pk = patient_id)
      context = RequestContext(request, {'patient_detail_obj': patient_detail_obj})

      if not getattr(patient_detail_obj,'urls',None):
        print "No Attribute of URLS on Patient. Saving to generate the same"
        patient_detail_obj.save()

      try:
        pane_template = Template( open('history/medical_history/dijit_widgets/pane.yaml','r').read() )

      except( IOError ):
        raise Http404("No template file to render the pane ! ")

      rendered_pane = pane_template.render(context)
      pane_yaml = yaml.load( rendered_pane ) 

      app_object = {}
      app_object['app'] = MODULE_LABEL
      app_object['ui_sections'] = {
                                  'app_type': 'main_module',
                                  'load_after': 'patient',
                                  'load_first': False,
                                  'layout'  :['trailing','top','center'],
                                  'widgets' :{ 'tree'    : None,
                                              'summary'  : None,
                                              'grid'     : None,
                                              'search'   : None
                                              }
                                  }
      app_object['url'] = None
      app_wrapper.append( app_object )

      success = True
      error_message = "Returning "+ MODULE_LABEL + " app pane variables"

      data = {'success': success,'error_message':error_message,'app': app_wrapper,'pane': pane_yaml}
      json  = simplejson.dumps(data)

      return HttpResponse(json, content_type="application/json")

    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Bad Request Parameters")

    except (PatientDetail.DoesNotExist):
      raise Http404("Bad Request: Patient Does Not Exist")
  
  else:
    raise Http404("Bad Request Method")