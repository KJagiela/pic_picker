from django.db import models


def entry_path(instance: 'ChallengeEntry', filename: str) -> str:
    return f'entry/challenge_{instance.challenge.id}/{filename}'


class Challenge(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.owner}'s {self.name} challenge"


class PhotoSubject(models.Model):
    challenge = models.ForeignKey('challenges.Challenge', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name} for {self.challenge}'


class ChallengeEntry(models.Model):
    photo = models.ImageField(upload_to=entry_path)
    subject = models.ForeignKey('challenges.PhotoSubject', on_delete=models.CASCADE)
    challenge = models.ForeignKey('challenges.Challenge', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.owner}'s entry in {self.subject} category for {self.challenge}"
