from django.conf.urls import url


from . import views

app_name='chembase'
urlpatterns= [
    url(r'^$',views.index,name='index'),
    url(r'^cmpd/(?P<cmpd_id>[0-9]+)/$',views.detail,name='detail'),
    url(r'^search/$',views.search_view,name='search'),
    url(r'^search_ajax/$',views.search_ajax,name='search_ajax'),
    url(r'^search_ajax_chemspy/$',views.chemspy_ajax,name='chemspy_ajax'),
    url(r'^structure_ajax/$',views.structure_ajax,name='structure_ajax'),
    url(r'^image_ajax/$',views.image_ajax,name='image_ajax'),
    url(r'^formula_ajax/$',views.formula_ajax,name='formula_ajax'),
    url(r'^sds_ajax/$',views.sds_ajax,name='sds_ajax'),
    url(r'^ghs_class_ajax/$',views.ghs_classes_transl,name='ghs_class_ajax'),
    url(r'^add/cmpd/$',views.add_cmpd,name='add_cmpd'), 
    url(r'^add/cmpd/done/$',views.cmpd_save,name='cmpd_save'), 
    url(r'^add/$',views.add,name='add'),
    

] 
