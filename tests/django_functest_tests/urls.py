import django
from django.contrib import admin

try:
    from django.urls import include, path

    url = None
except ImportError:
    path = None
    from django.conf.urls import url, include

from . import views

if path is None:
    urlpatterns = [
        url(r"^admin/", admin.site.urls),
        url(r"^django_functest/", include("django_functest.urls")),
        url(r"^test_misc/", views.test_misc, name="test_misc"),
        url(
            r"^redirect_to_misc/",
            views.redirect_to_misc,
            name="redirect_to_misc",
        ),
        url(
            r"^set_sess_foo_to_bar/",
            views.set_sess_foo_to_bar,
            name="set_sess_foo_to_bar",
        ),
        url(r"^list_things/", views.list_things, name="list_things"),
        url(r"^edit_thing/(?P<thing_id>.*)/", views.edit_thing, name="edit_thing"),
        url(
            r"^edit_thing_with_upload/(?P<thing_id>.*)/",
            views.edit_thing_with_upload,
            name="edit_thing_with_upload",
        ),
        url(
            r"^thing_cleared/(?P<thing_id>.*)/",
            views.thing_cleared,
            name="thing_cleared",
        ),
        url(
            r"^new_browser_session_test/",
            views.new_browser_session_test,
            name="new_browser_session_test",
        ),
    ]
else:
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("django_functest/", include("django_functest.urls")),
        path("test_misc/", views.test_misc, name="test_misc"),
        path(
            "redirect_to_misc/",
            views.redirect_to_misc,
            name="redirect_to_misc",
        ),
        path(
            "set_sess_foo_to_bar/",
            views.set_sess_foo_to_bar,
            name="set_sess_foo_to_bar",
        ),
        path("list_things/", views.list_things, name="list_things"),
        path("edit_thing/<str:thing_id>/", views.edit_thing, name="edit_thing"),
        path(
            "edit_thing_with_upload/<str:thing_id>/",
            views.edit_thing_with_upload,
            name="edit_thing_with_upload",
        ),
        path("thing_cleared/<str:thing_id>/", views.thing_cleared, name="thing_cleared"),
        path(
            "new_browser_session_test/",
            views.new_browser_session_test,
            name="new_browser_session_test",
        ),
    ]

if django.VERSION < (1, 9):
    from django.conf.urls import patterns

    urlpatterns = patterns("", *urlpatterns)
