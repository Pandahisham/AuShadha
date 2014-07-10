from django.conf.urls import *
from django.contrib import admin
import AuShadha.settings
admin.autodiscover()

from .views import fda_drug_db_json_all_drugs, fda_drug_db_json_for_a_drug, fda_drug_db_search, fda_drug_db_advanced_search, fda_drug_summary

from dijit_widgets.pane import render_fda_drug_db_pane
from dijit_widgets.tree import render_fda_drug_db_tree


urlpatterns = patterns('',
        

	url(r'render/pane/$', render_fda_drug_db_pane, name = 'render_fda_drug_db_pane'),
	url(r'render/tree/$', render_fda_drug_db_tree, name = 'render_fda_drug_db_tree'),

	url(r'json/all_drugs/$', fda_drug_db_json_all_drugs, name = 'fda_drug_db_json_all_drugs'),
	url(r'json_for_a_drug/(?P<drug_id>\d+)/$', fda_drug_db_json_for_a_drug, name = 'fda_drug_db_json_for_a_drug'),
	url(r'summary/(?P<drug_id>\d+)/$', fda_drug_summary, name = 'fda_drug_summary'),

	url(r'search/$', fda_drug_db_search, name = 'fda_drug_db_search'),
	url(r'advanced_search/$', fda_drug_db_advanced_search, name = 'fda_drug_db_advanced_search'),
	url(r'advanced_search/$', fda_drug_db_advanced_search, name = 'fda_drug_db_advanced_search'),

)


