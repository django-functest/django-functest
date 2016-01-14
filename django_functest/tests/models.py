from django.db import models


# After making changes here, run:
#   ./runtests.py --update-migration
class Thing(models.Model):
    name = models.CharField(max_length=255)
