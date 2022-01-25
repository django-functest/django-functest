import django

try:
    from django.urls import path

    url = None
except ImportError:
    path = None
    from django.conf.urls import url

from django.http import HttpResponse


def emptypage(request):
    # Minimal page needed for some tests.

    # We include a favicon link to stop browsers making a request to
    # /favicon.ico which slows things down (potentially a lot) and can cause
    # other issues.
    return HttpResponse(
        """<html>
    <head>
        <link href="data:image/gif;base64,R0lGODlhEAAQAIABAACE/////yH5BAEKAAEALA"""
        """AAAAAQABAAAAIghI9pwe2+nmRxvmobzmFnb4GTKJEXwEFoSq2sqSqyUQAAOw==" rel="shortcut icon">
    </head>
    <body></body>
</html>"""
    )


if path is None:
    urlpatterns = [
        url(r"^__emptypage/$", emptypage, name="django_functest.emptypage"),
    ]
else:
    urlpatterns = [
        path(r"__emptypage/", emptypage, name="django_functest.emptypage"),
    ]


if django.VERSION < (1, 9):
    from django.conf.urls import patterns

    urlpatterns = patterns("", *urlpatterns)
