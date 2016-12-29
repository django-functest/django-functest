from __future__ import absolute_import, print_function, unicode_literals

import django
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django_functest/', include('django_functest.urls')),
    url(r'^test_misc/', views.test_misc, name='django_functest.test_misc'),
    url(r'^set_sess_foo_to_bar/', views.set_sess_foo_to_bar, name='django_functest.set_sess_foo_to_bar'),
    url(r'^list_things/', views.list_things, name='list_things'),
    url(r'^edit_thing/(?P<thing_id>.*)/', views.edit_thing, name='edit_thing'),
    url(r'^edit_thing_with_upload/(?P<thing_id>.*)/', views.edit_thing_with_upload, name='edit_thing_with_upload'),
    url(r'^thing_cleared/(?P<thing_id>.*)/', views.thing_cleared, name='thing_cleared'),
]

if django.VERSION < (1, 9):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
