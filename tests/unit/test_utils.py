import pytest

from starwars.characters.models import Character
from starwars.characters.utils import import_characters


@pytest.fixture
def character_data():
    return [
        {
            "id": 1,
            "name": "Luke Skywalker",
            "height": 1.72,
            "mass": 73,
            "gender": "male",
            "homeworld": "tatooine",
            "born": -19,
            "species": "human",
            "hairColor": "blond",
            "eyeColor": "blue",
            "skinColor": "light",
            "cybernetics": "Prosthetic right hand",
            "affiliations": ["Resistance"],
            "masters": ["Yoda"],
            "apprentices": ["Rey"],
            "formerAffiliations": [],
        },
        {
            "id": 2,
            "name": "Darth Vader",
            "height": 2.03,
            "mass": 120,
            "gender": "male",
            "homeworld": "tatooine",
            "born": -41,
            "died": 4,
            "species": "human",
            "hairColor": "blond",
            "eyeColor": "blue",
            "skinColor": "light",
            "cybernetics": "Cybernetic right arm; later prosthetic arms and legs, and a life-support system",  # noqa
            "affiliations": ["Imperial High Command"],
            # Test with a single master
            "masters": "Yoda (Force spirit teacher)",
            "apprentices": ["Inquisitorius"],
            "formerAffiliations": [],
        },
    ]


@pytest.mark.django_db
def test_import_characters(character_data):
    import_characters(character_data)

    luke = Character.objects.get(name="Luke Skywalker")
    vader = Character.objects.get(name="Darth Vader")

    assert luke.name == "Luke Skywalker"
    assert luke.height == 1.72
    assert luke.mass == 73
    assert luke.gender == "male"
    assert luke.homeworld == "tatooine"
    assert luke.born == -19
    assert luke.species == "human"
    assert luke.hair_color == "blond"
    assert luke.eye_color == "blue"
    assert luke.skin_color == "light"
    assert luke.attributes["cybernetics"] == "Prosthetic right hand"
    assert luke.affiliations.filter(name="Resistance").exists()
    assert luke.masters.filter(name="Yoda").exists()
    assert luke.apprentices.filter(name="Rey").exists()

    assert vader.name == "Darth Vader"
    assert vader.height == 2.03
    assert vader.mass == 120
    assert vader.gender == "male"
    assert vader.homeworld == "tatooine"
    assert vader.born == -41
    assert vader.died == 4
    assert vader.species == "human"
    assert vader.hair_color == "blond"
    assert vader.eye_color == "blue"
    assert vader.skin_color == "light"
    assert (
        vader.attributes["cybernetics"]
        == "Cybernetic right arm; later prosthetic arms and legs, and a life-support system"  # noqa
    )
    assert vader.affiliations.filter(name="Imperial High Command").exists()
    assert vader.masters.filter(name="Yoda").exists()
    assert vader.apprentices.filter(name="Inquisitorius").exists()


@pytest.mark.django_db
def test_import_characters_with_placeholders(character_data):
    character_data[0]["masters"] = ["Darth Sidious"]
    import_characters(character_data)

    luke = Character.objects.get(name="Luke Skywalker")
    sidious = Character.objects.get(name="Darth Sidious")

    assert luke.masters.filter(name="Darth Sidious").exists()
    assert sidious.is_placeholder is True
