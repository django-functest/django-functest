import django
from django.conf.urls import include, patterns, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django_functest/', include('django_functest.urls')),
    url(r'^test1/', views.test1, name='django_functest.test1'),
    url(r'^list_things/', views.list_things, name='list_things'),
    url(r'^edit_thing/(?P<thing_id>.*)/', views.edit_thing, name='edit_thing'),
]

if django.VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
