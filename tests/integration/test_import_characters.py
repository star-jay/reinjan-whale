import pytest
from django.core.management import call_command

from starwars.characters.models import Affiliation, Character


@pytest.mark.django_db
def test_import_characters():

    call_command("import_characters", "starwars-data.json")

    assert Character.objects.exclude(is_placeholder=True).count() == 87
    assert Affiliation.objects.count() == 140
    assert Character.objects.first().affiliations.count() == 10

    assert Character.objects.first().born == -19
    assert Character.objects.first().died == 34
    # assert Character.objects.first().died_location == "Death Star II"
    assert Character.objects.first().homeworld == "tatooine"
