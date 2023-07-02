from django.contrib import admin

from apps.challenges import models


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'owner')
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


class ChallengeEntryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner', 'votes_count')
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    @admin.display(empty_value='0')
    def votes_count(self, obj):
        return obj.voters.count()


admin.site.register(models.Challenge, ChallengeAdmin)
admin.site.register(models.PhotoSubject)
admin.site.register(models.ChallengeEntry, ChallengeEntryAdmin)
