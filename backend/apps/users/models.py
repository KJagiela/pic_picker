from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    deleted = models.BooleanField(default=False)

    def delete(
        self,
        using: Any = ...,
        keep_parents: bool = ...,
        force: bool = False,
    ) -> tuple[int, dict[str, int]] | None:
        if force:
            return super().delete(using, keep_parents)
        self.deleted = True
        self.username = '_deleted_'
        self.email = 'deleted@example.com'
        self.save(update_fields=['deleted', 'username', 'email'])
