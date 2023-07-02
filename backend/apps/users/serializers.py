from rest_framework import serializers

from apps.challenges.serializers import ChallengeEntrySerializer
from apps.users.models import UserVote


class UserVoteSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name')
    entries = ChallengeEntrySerializer(source='subject.entries', many=True)
    chosen_entry = serializers.UUIDField(source='entry.id')

    class Meta:
        model = UserVote
        fields = (
            'subject_name',
            'entries',
            'chosen_entry',
        )
