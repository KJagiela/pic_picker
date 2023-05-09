import pytest

from ...users.tests.factories import UserFactory
from ..models import entry_path
from .factories import (
    ChallengeEntryFactory,
    ChallengeFactory,
    PhotoSubjectFactory,
)


def test_entry_path(db):
    entry = ChallengeEntryFactory()
    actual = entry_path(entry, 'test.png')
    assert actual == f'entry/challenge_{entry.subject.challenge.id}/test.png'


@pytest.mark.django_db
class TestString:
    def test_challenge_string(self):
        owner = UserFactory(username='kasia')
        challenge = ChallengeFactory(owner=owner, name='my challenge')
        assert str(challenge) == "kasia's my challenge challenge"

    def test_subject_string(self):
        owner = UserFactory(username='kasia')
        challenge = ChallengeFactory(owner=owner, name='my challenge')
        subject = PhotoSubjectFactory(challenge=challenge, name='test')
        assert str(subject) == "test for kasia's my challenge challenge"

    def test_entry_string(self):
        owner = UserFactory(username='kasia')
        challenge = ChallengeFactory(owner=owner, name='my challenge')
        subject = PhotoSubjectFactory(challenge=challenge, name='test')
        entry = ChallengeEntryFactory(subject=subject, owner=owner)
        assert (
            str(entry)
            == "kasia's entry in category test for kasia's my challenge challenge"
        )
