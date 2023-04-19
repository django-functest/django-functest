from django.contrib import admin
from django.urls import include, path

from . import views

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
    path("new_browser_session_test/", views.new_browser_session_test, name="new_browser_session_test"),
    path(r"auto_submit_form/", views.auto_submit_form, name="auto_submit_form"),
    path(r"delayed_appearance/", views.delayed_appearance, name="delayed_appearance"),
    path(r"overflowing/", views.overflowing, name="overflowing"),
    path(r"long_page/", views.long_page, name="long_page"),
    path(r"with_confirm", views.with_confirm, name="with_confirm"),
    path(r"web_components/", views.web_components, name="web_components"),
]
