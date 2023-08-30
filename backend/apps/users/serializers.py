from rest_framework import serializers

from apps.challenges.serializers import ChallengeEntrySerializer
from apps.users.models import UserVote


class UserVoteSerializer(serializers.ModelSerializer):
    chosen_entry = serializers.UUIDField(source='entry.id')

    class Meta:
        model = UserVote
        fields = (
            'chosen_entry',
        )

