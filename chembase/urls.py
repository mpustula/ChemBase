from django.conf.urls import url


from . import views

app_name='chembase'
urlpatterns= [
    url(r'^$',views.index,name='index'),
    url(r'^cmpd/(?P<cmpd_id>[0-9]+)/$',views.detail,name='detail'),
    url(r'^search/$',views.search,name='search'),
    url(r'^add/$',views.add,name='add')

] 
