from django.db import models


# After making changes here, run:
#   ./runtests.py updatemigration
class Thing(models.Model):
    name = models.CharField(max_length=255)
