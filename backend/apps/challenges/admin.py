from django.contrib import admin

from . import models


class ChallengeAdmin(admin.ModelAdmin):
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


class ChallengeEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


admin.site.register(models.Challenge, ChallengeAdmin)
admin.site.register(models.PhotoSubject)
admin.site.register(models.ChallengeEntry, ChallengeEntryAdmin)
