import pytest

from tests.factories import CharacterFactory


@pytest.mark.django_db
def test_character_is_evil():
    character = CharacterFactory()

    assert character.is_evil is False, "A random character should not be evil"


@pytest.mark.django_db
def test_character_is_evil_darth_or_sith():
    character = CharacterFactory(name="Darth Vader")
    assert character.is_evil is True, "A character with Darth in the name should be evil" # noqa

    character = CharacterFactory(name="Sith Lord")
    assert character.is_evil is True, "A character with Sith in the name should be evil" # noqa


@pytest.mark.django_db
def test_character_is_evil_affiliation():
    character = CharacterFactory()
    character.affiliations.create(name="Sith")

    assert character.is_evil is True, "A character with Sith affiliation should be evil" # noqa


@pytest.mark.django_db
def test_character_is_evil_master():
    character = CharacterFactory()
    master = CharacterFactory(name="Darth Sidious")
    character.masters.add(master)

    assert character.is_evil is True, "A character with Darth in the master name should be evil" # noqa