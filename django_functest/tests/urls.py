import django
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^django_functest/', include('django_functest.urls'))
                       )

if django.VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
