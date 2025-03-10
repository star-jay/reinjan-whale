from rest_framework import validators


def no_evil_character_validator(value):
    """
    Validate that the character is not evil.
    """
    # No evil members are allowed
    if value.is_evil:
        raise validators.ValidationError(
            'Evil members are not allowed.')
    return value


def team_member_count_validator(value):
    """
    Validate that the team has at most 5 members.
    """
    if value.members.count() >= 5:
        raise validators.ValidationError(
            'A team can have at most 5 members')
    return value
