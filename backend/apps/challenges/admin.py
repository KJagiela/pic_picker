from django.contrib import admin
from . import models

admin.site.register(models.Challenge)
admin.site.register(models.PhotoSubject)
admin.site.register(models.ChallengeEntry)
