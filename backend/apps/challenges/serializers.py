import random
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
        # TODO: cloudinary transformation
        return obj.photo.build_url()


class ChallengeEntryResultsSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    class Meta:
        model = models.ChallengeEntry
        fields = ('id', 'photo', 'votes')

    def get_photo(self, obj):
        return obj.photo.build_url(width='200')

    def get_votes(self, obj):
        return random.randint(0, 10)

class PhotoSubjectSerializer(serializers.ModelSerializer):
    entries = ChallengeEntrySerializer(many=True)

    class Meta:
        model = models.PhotoSubject
        fields = (
            'id',
            'name',
            'entries',
        )
