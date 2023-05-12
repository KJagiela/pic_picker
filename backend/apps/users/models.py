from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    deleted = models.BooleanField(default=False)

    def delete(  # type: ignore[override]
        self,
        using: Any = None,
        keep_parents: bool = False,
        force: bool = False,
    ) -> tuple[int, dict[str, int]] | None:
        if force:
            return super().delete(using, keep_parents)
        self.deleted = True
        self.username = '_deleted_'
        self.email = 'deleted@example.com'
        self.save(update_fields=['deleted', 'username', 'email'])


class UserVotes(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='votes',
    )
    subject = models.ForeignKey(
        'challenges.PhotoSubject',
        on_delete=models.CASCADE,
        related_name='participants',
    )
    entry = models.ForeignKey(
        'challenges.ChallengeEntry',
        on_delete=models.CASCADE,
        related_name='voters',
    )

    class Meta:
        unique_together = ('user', 'subject')

    def clean(self) -> None:
        if self.entry.subject_id != self.subject_id:
            raise ValidationError("Subject is different than the entry's subject")
