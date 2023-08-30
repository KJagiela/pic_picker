import random
from collections import defaultdict

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.challenges.models import Challenge, ChallengeEntry
from apps.challenges.serializers import PhotoSubjectSerializer, ChallengeEntryResultsSerializer
from apps.users.models import UserVote
from apps.users.serializers import UserVoteSerializer


class PicPickerView(APIView):
    def get(self, request: Request, *args, **kwargs):
        challenge_id = request.GET.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        subjects = (
            challenge.subjects.exclude(voters=request.user)
            .annotate(no_entries=Count('entries'))
            .filter(no_entries__gt=0)
        )
        try:
            current_subject = random.choice(subjects)
        except IndexError:
            return Response(
                {'msg': 'No more subjects to rate'},
                # incorrect, I know. But funny and won't be confused ;)
                status=status.HTTP_226_IM_USED,
            )
        serializer_data = PhotoSubjectSerializer(
            current_subject,
            context={'request': request},
        ).data
        random.shuffle(serializer_data['entries'])
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


class ResultsView(APIView):
    # TODO: security - can't see if you have unrated photos
    def get(self, request: Request, *args, **kwargs):

        challenge_id = request.GET.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        subjects = challenge.subjects.all()
        entries = ChallengeEntry.objects.filter(subject__in=subjects)

        serialized_entries = defaultdict(defaultdict)
        for entry in entries:
            serialized_entry = ChallengeEntryResultsSerializer(entry)
            serialized_entries[str(entry.subject.name)][entry.owner_id] = serialized_entry.data

        chosen_entries = list(
            UserVote.objects.filter(user=request.user).values_list('entry_id', flat=True)
        )

        owners = list(UserVote.objects.filter(entry__in=entries).values('entry__owner_id').annotate(score=Count('id')))

        return Response(data={'subjects': serialized_entries, 'chosen': chosen_entries, 'owners': owners})
