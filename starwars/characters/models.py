from django.db import models, transaction
from django.db.models import Q


class Affiliation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GenderChoices(models.TextChoices):
    male = "male"
    female = "female"
    other = "other"


class CharacterManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    @transaction.atomic
    def create_character(self, **kwargs):
        """
        Create a character and its (former) affiliations.
        """

        affiliations = kwargs.pop("affiliations", [])
        former_affiliations = kwargs.pop("former_affiliations", [])
        # Link to other characters, don't create them until all Characters
        # are created
        _masters = kwargs.pop("masters", [])
        _apprentices = kwargs.pop("apprentices", [])

        character = self.create(**kwargs)

        for affiliation_name in affiliations:
            affiliation, _c = Affiliation.objects.get_or_create(
                name=affiliation_name)
            character.affiliations.add(affiliation)

        for affiliation_name in former_affiliations:
            affiliation, _c = Affiliation.objects.get_or_create(
                name=affiliation_name)
            character.former_affiliations.add(affiliation)

        return character


class Character(models.Model):
    """
    Model for a Star Wars character.

    Fields:

    "id": 87,
    "name": 87,
    "height": 86,
    "mass": 64,
    "gender": 87,
    "homeworld": 81,
    "wiki": 87,
    "image": 87,
    "born": 47,
    "died": 47,
    "diedLocation": 44,
    "species": 87,
    "hairColor": 48,
    "eyeColor": 87,
    "skinColor": 85,
    "affiliations": 87,
    "formerAffiliations": 87,
    "masters": 15,
    "apprentices": 12,
    """

    affiliations = models.ManyToManyField(
        "Affiliation",
        related_name="characters",
        help_text="Affiliations of the character",
    )
    attributes = models.JSONField(
        help_text="Extra defining attributes of the character",
        default=dict,
        null=True,
    )
    born = models.IntegerField(
        help_text="Year the character was born", null=True
    )
    died = models.IntegerField(
        help_text="Year the character is deceased", null=True
    )
    died_location = models.CharField(
        max_length=255, help_text="Location where the character died", null=True
    )
    eye_color = models.CharField(
        max_length=255, help_text="Eye color of the character", null=True
    )
    former_affiliations = models.ManyToManyField(
        "Affiliation",
        related_name="former_characters",
        help_text="Former affiliations of the character",
    )
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=10,
        help_text="Gender of the character",
        null=True,
    )
    hair_color = models.CharField(
        max_length=255, help_text="Hair color of the character", null=True
    )
    height = models.FloatField(help_text="Height of the character", null=True)
    homeworld = models.CharField(
        max_length=255, help_text="Homeworld of the character", null=True
    )
    image = models.URLField(help_text="URL to the character's image", null=True)
    is_placeholder = models.BooleanField(
        help_text="Placeholder character referenced by other characters",
        default=False
    )
    mass = models.FloatField(help_text="Mass of the character", null=True)
    masters = models.ManyToManyField(
        "self",
        related_name="apprentices",
        symmetrical=False,
        help_text="Masters of the character",
    )
    name = models.CharField(
        max_length=255, help_text="Name of the character", null=True
    )

    reference_id = models.IntegerField(
        help_text="Reference ID of the character",
        null=True,
        unique=True,
    )
    skin_color = models.CharField(
        max_length=255, help_text="Skin color of the character", null=True
    )
    species = models.CharField(
        max_length=255, help_text="Species of the character", null=True
    )
    wiki = models.URLField(
        help_text="URL to the character's wiki page", null=True
    )

    objects = CharacterManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

    @property
    def is_evil(self):
        """
        Returns True if the character is evil.

        A character is considered evil if:

        They have ‘Darth’ or ‘Sith’ in their name
        They have at least one affiliation that mentions ‘Darth’ or ‘Sith’
        (you may ignore former affiliations)
        They have at least one master with ‘Darth’ in their name
        """
        if "Darth" in self.name or "Sith" in self.name:
            return True
        if self.affiliations.filter(
            Q(name__icontains="Darth") | Q(name__icontains="Sith")
        ).exists():
            return True
        if self.masters.filter(name__icontains="Darth").exists():
            return True

        return self.affiliations.filter(name="Sith").exists()


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        "Character",
        related_name="teams",
        help_text="Members of the team",
        through="TeamMembership",
    )

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_memberships"
    )
    character = models.ForeignKey(
        "Character", on_delete=models.CASCADE, related_name="team_memberships"
    )

    class Meta:
        unique_together = ["team", "character"]
