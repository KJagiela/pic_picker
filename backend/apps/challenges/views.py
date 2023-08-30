import random
from collections import defaultdict

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.challenges.models import Challenge
from apps.challenges.serializers import PhotoSubjectSerializer
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
        # maybe DB design wasn't the greatest :thinking:
        entries = subjects.values_list('name', 'entries__owner__username', 'entries__photo', 'entries__id')
        serialized_entries = defaultdict(defaultdict)
        owners = set()
        for subject_name, entry_owner, entry_photo, entry_id in entries:
            if not entry_id:
                continue
            entry_photo_url = entry_photo.build_url(width='200')
            serialized_entries[subject_name][entry_owner] = {'id': entry_id, 'photo': entry_photo_url, 'votes': random.randint(0, 10)}
            owners.add(entry_owner)
        votes = UserVote.objects.filter(user=request.user).prefetch_related('entry')
        votes_serializer = UserVoteSerializer(votes, many=True)
        chosen_ids = [chosen['chosen_entry'] for chosen in votes_serializer.data]
        owners = [{'id': owner} for owner in owners]
        for owner in owners:
            owner['score'] = UserVote.objects.filter(entry__owner__username=owner['id']).count()
        
        return Response(data={'subjects': dict(serialized_entries), 'chosen': chosen_ids, 'owners': owners})
