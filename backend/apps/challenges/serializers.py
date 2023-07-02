from rest_framework import serializers

from apps.challenges import models


class ChallengeEntrySerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = models.ChallengeEntry
        fields = (
            'id',
            'photo',
        )

    def get_photo(self, obj):
        return obj.photo.build_url()


class ChallengeEntryResultsSerializer(ChallengeEntrySerializer):
    votes_count = serializers.SerializerMethodField

    class Meta(ChallengeEntrySerializer.Meta):
        fields = ChallengeEntrySerializer.Meta.fields + ('votes_count',)


class PhotoSubjectSerializer(serializers.ModelSerializer):
    entries = ChallengeEntrySerializer(many=True)

    class Meta:
        model = models.PhotoSubject
        fields = (
            'id',
            'name',
            'entries',
        )
