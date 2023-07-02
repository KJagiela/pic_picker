import uuid

from django.conf import settings
from django.db import models

from cloudinary.models import CloudinaryField


def entry_path(instance: 'ChallengeEntry', filename: str) -> str:
    return f'entry/challenge_{instance.subject.challenge.id}/{filename}'


class ChallengeEntryCloudinaryField(CloudinaryField):
    def pre_save(self, model_instance, add):
        self.options['folder'] = (
            f'{settings.CLOUDINARY_FOLDER}/'
            + f'challenge_{model_instance.subject.challenge.id}/'
        )
        return super().pre_save(model_instance, add)


class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='challenges',
    )

    def __str__(self) -> str:
        return f"{self.owner}'s {self.name} challenge"


class PhotoSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(
        'challenges.Challenge',
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    name = models.CharField(max_length=256)
    voters = models.ManyToManyField(to='users.User', through='users.UserVote')

    def __str__(self):
        return f'{self.name} for {self.challenge}'


class ChallengeEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = ChallengeEntryCloudinaryField('image')
    subject = models.ForeignKey(
        'challenges.PhotoSubject',
        on_delete=models.CASCADE,
        related_name='entries',
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='entries',
    )

    def __str__(self):
        return f"{self.owner}'s entry in category {self.subject}"
