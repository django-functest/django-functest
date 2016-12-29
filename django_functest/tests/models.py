from __future__ import absolute_import, print_function, unicode_literals

from django.db import models

UPLOAD_DIR = "django_functest/tests/uploads"


# After making changes here, run:
#   ./runtests.py --update-migration
class Thing(models.Model):
    ELEMENT_EARTH = 'e'
    ELEMENT_WATER = 'w'
    ELEMENT_AIR = 'a'
    ELEMENT_FIRE = 'f'
    ELEMENT_CHOICES = [
        (ELEMENT_EARTH, 'Earth'),
        (ELEMENT_WATER, 'Water'),
        (ELEMENT_AIR, 'Air'),
        (ELEMENT_FIRE, 'Fire')
    ]

    CATEGORY_MAGMA = 0
    CATEGORY_QUASIGROUP = 1
    CATEGORY_MONOID = 2
    CATEGORY_CHOICES = [
        (CATEGORY_MAGMA, 'Magma'),
        (CATEGORY_QUASIGROUP, 'Quasigroup'),
        (CATEGORY_MONOID, 'Monoid'),
    ]

    name = models.CharField(max_length=255)
    big = models.BooleanField(default=False)
    clever = models.BooleanField(default=False)
    element_type = models.CharField(max_length=1,
                                    choices=ELEMENT_CHOICES)
    category = models.IntegerField(choices=CATEGORY_CHOICES,
                                   default=CATEGORY_MAGMA)
    count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    notes_file = models.FileField(blank=True, upload_to=UPLOAD_DIR)
