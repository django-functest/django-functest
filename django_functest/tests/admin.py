from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from .models import Thing

admin.site.register(Thing)
