from django.conf.urls import url
from django.contrib.auth import views as auth_views

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
    url(r'^add/item/cmpd/(?P<cmpd_id>[0-9]+)/$',views.add_item,name='add_item'),
    url(r'^add/$',views.add,name='add'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='chembase/login.html'),name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^accounts/profile',views.account_view,name='account'),
    url(r'^change-password/$', auth_views.PasswordChangeView.as_view(template_name='chembase/change_password.html',success_url='/change-password-done'),name='change_password'),
    url(r'^change-password-done/$', auth_views.PasswordChangeDoneView.as_view(template_name='chembase/change_password_done.html'),name='password_change_done'),
    

] 
