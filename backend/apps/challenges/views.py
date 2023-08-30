import random
from collections import defaultdict

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

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


class ResultsView(ListAPIView):
    # TODO: security - can't see if you have unrated photos
    serializer_class = ChallengeEntryResultsSerializer

    def get_queryset(self):
        challenge_id = self.request.GET.get('challenge_id')
        challenge = get_object_or_404(Challenge, id=challenge_id)
        subjects = challenge.subjects.all()
        entries = ChallengeEntry.objects.filter(subject__in=subjects).annotate(score=Count('voters'))
        return entries

    def reformat_serialized_entries(self, serialized_entries):
        reformatted_entries = defaultdict(defaultdict)
        for entry in serialized_entries:
            name = entry.pop('subject_name')
            owner = entry.pop('owner')
            reformatted_entries[name][owner] = entry
        return reformatted_entries

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        chosen_entries = list(
            UserVote.objects.filter(user=request.user).values_list('entry_id', flat=True)
        )
        owners = list(UserVote.objects.filter(entry__in=self.get_queryset()).values('entry__owner__username').annotate(score=Count('id')))
        for owner in owners:
            owner['name'] = owner.pop('entry__owner__username')
        response.data = {'subjects': self.reformat_serialized_entries(response.data), 'chosen': chosen_entries, 'owners': owners}
        return response
