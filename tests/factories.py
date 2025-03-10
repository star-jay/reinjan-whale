import factory

from starwars.accounts.models import User
from starwars.characters.models import Affiliation, Character, Team


class AffiliationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Affiliation

    name = factory.Faker("word")


class CharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    name = factory.Faker("name")
    height = factory.Faker("random_int", min=100, max=250)
    mass = factory.Faker("random_int", min=50, max=200)


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker("word")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    is_staff = False
    is_superuser = False
    password = factory.Faker("password")
