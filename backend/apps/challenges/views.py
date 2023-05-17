import random

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.challenges.models import Challenge
from apps.challenges.serializers import PhotoSubjectSerializer
from apps.users.models import UserVote


class PicPickerView(APIView):
    def get(self, request: Request, *args, **kwargs):
        challenge_id = request.GET.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        subjects = (
            challenge.subjects.exclude(voters=request.user)
            .annotate(no_entries=Count('entries'))
            .filter(no_entries__gt=0)
        )
        current_subject = random.choice(subjects)
        serializer_data = PhotoSubjectSerializer(
            current_subject,
            context={'request': request},
        ).data
        return Response(serializer_data)


class RegisterVoteView(APIView):
    def post(self, request: Request, *args, **kwargs):
        subject_id = request.data.get('subject_id')
        entry_id = request.data.get('entry_id')

        UserVote.objects.create(
            user=request.user,
            subject_id=subject_id,
            entry_id=entry_id,
        )
        return Response()
