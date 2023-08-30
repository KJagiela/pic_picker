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
    score = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.username')
    subject_name = serializers.CharField(source='subject.name')

    class Meta:
        model = models.ChallengeEntry
        fields = ['id', 'owner', 'subject', 'score', 'photo', 'subject_name']

    def get_score(self, obj):
        return obj.score

    def get_photo(self, obj):
        return obj.photo.build_url(width='200')

class PhotoSubjectSerializer(serializers.ModelSerializer):
    entries = ChallengeEntrySerializer(many=True)

    class Meta:
        model = models.PhotoSubject
        fields = (
            'id',
            'name',
            'entries',
        )
