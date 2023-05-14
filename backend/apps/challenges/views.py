import random

from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.challenges.models import Challenge
from apps.challenges.serializers import PhotoSubjectSerializer


class PicPickerView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        challenge_id = self.request.GET.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        subjects = (
            challenge.subjects.exclude(voters=request.user)
            .annotate(no_entries=Count('entries'))
            .filter(no_entries__gt=0)
        )
        current_subject = random.choice(subjects)
        serializer_data = PhotoSubjectSerializer(
            current_subject, context={'request': self.request}
        ).data
        return Response(serializer_data)
