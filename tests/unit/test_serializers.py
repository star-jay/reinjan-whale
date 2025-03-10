import pytest

from starwars.characters.serializers import TeamMembershipSerializer
from tests.factories import CharacterFactory, TeamFactory


@pytest.mark.django_db
def test_team_serializer_validate_member_count():
    team = TeamFactory()

    serializer = TeamMembershipSerializer(
        data={
            "team_id": team.id,
            "character_id": CharacterFactory().id,
        }
    )
    assert serializer.is_valid() is True, f"You can add a member to an empty team {serializer.errors}"  # noqa

    # Add 4 members
    team.members.add(CharacterFactory())
    team.members.add(CharacterFactory())
    team.members.add(CharacterFactory())
    team.members.add(CharacterFactory())

    serializer = TeamMembershipSerializer(
        data={
            "team_id": team.id,
            "character_id": CharacterFactory().id,
        }
    )
    assert serializer.is_valid() is True, f"You can add the 5th member {serializer.errors}" # noqa

    # Add 5th member
    team.members.add(CharacterFactory())

    serializer = TeamMembershipSerializer(
        data={
            "team_id": team.id,
            "character_id": CharacterFactory().id,
        }
    )
    assert serializer.is_valid() is False, f"A team with 6 members is not valid {serializer.errors}" # noqa


@pytest.mark.django_db
def test_team_serializer_no_evil_members():
    serializer = TeamMembershipSerializer(
        data={
            "name": "Sad Team",
            "member_ids": [
                CharacterFactory(name="Darth Vader").id,
                CharacterFactory(name="Luke Skywalker").id,
            ]
        }
    )
    assert serializer.is_valid() is False, f"A team with evil members is not valid {serializer.errors}" # noqa
