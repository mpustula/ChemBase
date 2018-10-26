from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name='chembase'
urlpatterns= [
    url(r'^$',views.index,name='index'),
    url(r'^sds/$',views.sds_index,name='sds_index'),
    url(r'^cmpd/(?P<cmpd_id>[0-9]+)/$',views.detail,name='detail'),
    url(r'^search/$',views.search_view,name='search'),
    url(r'^search_ajax/$',views.search_ajax,name='search_ajax'),
    url(r'^search_ajax_chemspy/$',views.chemspy_ajax,name='chemspy_ajax'),
    url(r'^search_qt/$',views.search_qt,name='search_qt'),
    url(r'^search_rm/$',views.search_rm,name='search_rm'),
    url(r'^search_gr/$',views.search_groups,name='search_gr'),
    url(r'^structure_ajax/$',views.structure_ajax,name='structure_ajax'),
    url(r'^image_ajax/$',views.image_ajax,name='image_ajax'),
    url(r'^formula_ajax/$',views.formula_ajax,name='formula_ajax'),
    url(r'^properties_ajax/$',views.properties_ajax,name='properties_ajax'),
    url(r'^clean_str_ajax/$',views.clean_str_ajax,name='clean_str_ajax'),
    url(r'^sds_ajax/$',views.sds_ajax,name='sds_ajax'),
    url(r'^ghs_class_ajax/$',views.ghs_classes_transl,name='ghs_class_ajax'),
    url(r'^item_loc_filter/$',views.item_loc_filter,name='item_loc_filter'),
    url(r'^add/cmpd/$',views.add_cmpd,name='add_cmpd'), 
    url(r'^add/cmpd/done/$',views.cmpd_save,name='cmpd_save'),
    url(r'^add/item/done/$',views.item_save,name='item_save'),
    url(r'^add/item/cmpd/(?P<cmpd_id>[0-9]+)/$',views.add_item,name='add_item'),
    url(r'^add/item/(?P<item_id>[0-9]+)/done$',views.add_item_done,name='add_item_done'),
    url(r'^sug/loc/cmpd/$',views.suggest_loc,name='suggest_loc'),
    url(r'^item_orz/$',views.get_orz_details,name='item_orz_details'),
    url(r'^item_delete/$',views.item_delete,name='item_delete'),
    url(r'^add/$',views.add,name='add'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='chembase/login.html'),name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^accounts/profile',views.account_view,name='account'),
    url(r'^change-password/$', views.password_change,name='change_password'),
    url(r'^change-password-done/$', auth_views.PasswordChangeDoneView.as_view(template_name='chembase/change_password_done.html'),name='password_change_done'),
    url(r'^admin/main$',views.admin,name='admin'),
    url(r'^admin/logs$',views.logs,name='admin_logs'),
    url(r'^admin/users$',views.users,name='admin_users'),
    url(r'^admin/user/(?P<user_id>[0-9]+)/$',views.edit_user,name='admin_user'),
    url(r'^admin/user/save$',views.save_user,name='admin_user_save'),
    url(r'^admin/user/expire$',views.expire_passwords,name='admin_user_expire'),
    url(r'^admin/server$',views.server,name='admin_server'),
    url(r'^admin/settings$',views.settings,name='admin_settings'),
    url(r'^admin/items$',views.cmpds_items,name='admin_cmpds_items'),
    url(r'^status/$',views.status,name='server_status'),
    url(r'^items_groups/$',views.get_groups,name='get_groups'),
    url(r'^admin/group/(?P<group_id>[0-9]+)/$',views.group_details,name='admin_group'),
    url(r'^admin/logs/(?P<file_type>[a-z]+)/$',views.log_file,name='log_files'),
    url(r'^admin/orz$',views.orz_form,name='admin_orz'),
    url(r'^admin/usersgroups$',views.users_groups,name='admin_users_groups'),
    url(r'^admin/reset_password$',views.reset_password,name='admin_users_reset_pass'),
    url(r'^admin/group/(?P<group_id>[0-9]+)/edit$',views.edit_group,name='admin_group_edit'),
    url(r'^admin/group/save$',views.save_group,name='admin_group_save'),

] 
