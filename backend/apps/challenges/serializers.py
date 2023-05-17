from rest_framework import serializers

from apps.challenges import models


class ChallengeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChallengeEntry
        fields = (
            'id',
            'photo',
        )


class PhotoSubjectSerializer(serializers.ModelSerializer):
    entries = ChallengeEntrySerializer(many=True)

    class Meta:
        model = models.PhotoSubject
        fields = (
            'id',
            'name',
            'entries',
        )
