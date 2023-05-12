from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework import generics

from apps.challenges.models import (
    Challenge,
    ChallengeEntry,
)


class PicPickerView(generics.GenericAPIView):
    def get_queryset(self) -> QuerySet[ChallengeEntry]:
        challenge_id = self.request.data.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        challenge.subjects
