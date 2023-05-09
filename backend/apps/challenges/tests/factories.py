import factory

from apps.users.tests.factories import UserFactory


class ChallengeFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = 'challenges.Challenge'


class PhotoSubjectFactory(factory.django.DjangoModelFactory):
    challenge = factory.SubFactory(ChallengeFactory)

    class Meta:
        model = 'challenges.PhotoSubject'


class ChallengeEntryFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    subject = factory.SubFactory(PhotoSubjectFactory)

    class Meta:
        model = 'challenges.ChallengeEntry'
