import django
from django.conf.urls import patterns, url
from django.http import HttpResponse


def emptypage(request):
    # Minimal page needed for some tests
    return HttpResponse('<html><body></body></html>')


urlpatterns = [
    url(r'^__emptypage/$', emptypage, name='django_functest.emptypage'),
]

if django.VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
