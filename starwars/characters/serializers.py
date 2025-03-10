from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Affiliation,
    Character,
    Team,
    TeamMembership,
)
from .validators import no_evil_character_validator, team_member_count_validator


class AffiliationNestedSerializer(serializers.ModelSerializer):
    """
    Lightweight Serializer for the Affiliation model.
    """

    class Meta:
        model = Affiliation
        fields = [
            "id",
            "url",
            "name",
        ]


class CharacterNestedSerializer(serializers.ModelSerializer):
    """
    Lightweight Serializer for the Character model.
    """
    class Meta:
        model = Character
        fields = [
            "id",
            "url",
            "name",
        ]


class TeamNestedSerializer(serializers.ModelSerializer):
    """
    Lightweight Serializer for the Team model.
    """
    class Meta:
        model = Team
        fields = [
            "id",
            "url",
            "name",
        ]


class AffiliationListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Affiliation model.
    """
    characters = CharacterNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Affiliation
        fields = [
            "id",
            "url",
            "name",
            "characters",
        ]


class CharacterDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Serializer for the Character model.

    This serializer includes additional information about the character.
    """
    affiliations = AffiliationNestedSerializer(
        many=True, read_only=True)
    apprentices = CharacterNestedSerializer(many=True, read_only=True)
    masters = CharacterNestedSerializer(many=True, read_only=True)
    teams = TeamNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "url",
            "name",

            "height",
            "is_evil",
            "image",
            "mass",
            "wiki",

            "attributes",

            "affiliations",
            "apprentices",
            "masters",
            "teams",
        ]


class CharacterListSerializer(serializers.ModelSerializer):
    """
    """
    affiliations = AffiliationNestedSerializer(
        many=True, read_only=True)
    apprentices = CharacterNestedSerializer(many=True, read_only=True)
    masters = CharacterNestedSerializer(many=True, read_only=True)
    teams = TeamNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Character

        fields = [
            "id",
            "url",
            "name",

            "height",
            "image",
            "mass",
            "wiki",


            "attributes",

            "affiliations",
            "apprentices",
            "masters",
            "teams",
        ]


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """

    members = CharacterNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "url",
            "name",
            "members",
        ]


class TeamMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for the TeamMembership model.
    """
    # team = TeamNestedSerializer(read_only=True)
    # character = CharacterNestedSerializer(read_only=True)

    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        validators=[team_member_count_validator]
    )

    character_id = serializers.PrimaryKeyRelatedField(
        queryset=Character.objects.all(),
        source='character',
        validators=[no_evil_character_validator]
    )

    class Meta:
        model = TeamMembership
        fields = [
            "id",
            "url",

            "character_id",
            "team_id",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=TeamMembership.objects.all(),
                fields=['character_id', 'team_id'],
                message='Character is already a member of the team'
            )
        ]
