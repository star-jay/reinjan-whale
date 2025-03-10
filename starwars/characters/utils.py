import logging

from django.db import transaction

from .models import Character

logger = logging.getLogger(__name__)

character_attribute_mapping = {
    # Keep the original id
    "id": "reference_id",
    # snake_case the keys
    "eyeColor": "eye_color",
    "hairColor": "hair_color",
    "skinColor": "skin_color",
    "bornLocation": "born_location",
    "diedLocation": "died_location",
    "platingColor": "plating_color",
    "sensorColor": "sensor_color",
    "dateDestroyed": "date_destroyed",
    "destroyedLocation": "destroyed_location",
    "productLine": "product_line",
    "dateCreated": "date_created",
    "formerAffiliations": "former_affiliations",
}


def clean_name(name):
    """
    Clean a characters name.

    This function removes any additional information from the name, like
    titles or nicknames.
    """
    if "(" in name:
        strip_index = name.index("(") or -1
        name = name[:strip_index].strip()

    return name


def clean_character_data(field_names, **kwargs):
    """
    Imports a new character object from the provided attributes.

    The data is cleaned before creating the object. The following fields
    are removed from the kwargs:
    - affiliations
    - formerAffiliations
    - masters
    - apprentices

    If an attribute is not defined in the model, it will be stored in the
    attributes field.

    If the value does not match the field type, it will be stored in the
    attributes field.
    """
    clean_kwargs = {
        character_attribute_mapping.get(key, key): value
        for key, value in kwargs.items()
    }

    # additional attributes
    additional_attributes = [
        key for key in clean_kwargs.keys() if key not in field_names
    ]

    clean_kwargs["attributes"] = {}

    for key in additional_attributes:
        # TODO: snake_case the value
        # If the key is not a field name, store it in the attributes field
        clean_kwargs["attributes"][key] = clean_kwargs.pop(key)

    for key in clean_kwargs.keys():
        if key == "born":
            # Fix for situation where born is a string
            if type(clean_kwargs["born"]) is not int:
                clean_kwargs["born"] = None
                clean_kwargs["attributes"]["born"] = kwargs["born"]

        if key == "masters":
            # Fix for situation where masters is a string
            if type(clean_kwargs["masters"]) is not list:
                clean_kwargs["masters"] = [clean_kwargs["masters"]]

    return clean_kwargs


@transaction.atomic
def import_characters(character_data):
    """
    Import a list of characters into the database.

    :param
        character_data: a list of json objects with character attributes

    This is done in 2 phases:
    1. Create the character objects
    2. Link characters with each other

    """

    # What attributes to store in the model
    character_field_names = [
        field.name for field in Character._meta.get_fields()]

    cleaned_data = [
        clean_character_data(character_field_names, **attrs)
        for attrs in character_data
    ]

    _characters = [
        Character.objects.create_character(**clean_attrs)
        for clean_attrs in cleaned_data
    ]

    # Link characters with each other
    for attrs in cleaned_data:
        character = Character.objects.get(name=attrs["name"])

        if "masters" not in attrs:
            continue

        for name in attrs.get("masters", []):
            name = clean_name(name)

            logger.debug(f"Linking {character} to master '{name}'")
            master, created = Character.objects.get_or_create(
                name=name, defaults={"is_placeholder": True}
            )
            if created:
                logger.warning(f"Master {name} not found, created placeholder.")

            character.masters.add(master)

        if "apprentices" not in attrs:
            continue

        if type(attrs.get("apprentices")) is str:
            attrs["apprentices"] = [attrs["apprentices"]]

        for name in attrs.get("apprentices", []):
            name = clean_name(name)

            logger.debug(f"Linking {character} to apprentice '{name}'")

            apprentice, created = Character.objects.get_or_create(
                name=name, defaults={"is_placeholder": True}
            )
            if created:
                logger.warning(
                    f"Apprentice {name} not found, created placeholder."
                )

            character.apprentices.add(apprentice)
