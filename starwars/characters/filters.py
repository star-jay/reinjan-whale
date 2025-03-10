from django_filters import CharFilter, FilterSet

from .models import Character


class CharacterFilter(FilterSet):
    """
    FilterSet for the Character model.
    """

    affiliation_name = CharFilter(
        field_name="affiliations__name",
        lookup_expr="icontains",
        label="Affiliation",
    )
    former_affiliation_name = CharFilter(
        field_name="former_affiliations__name",
        lookup_expr="icontains",
        label="Former Affiliation",
    )

    died_location = CharFilter(lookup_expr="icontains")
    name = CharFilter(lookup_expr="icontains")
    species = CharFilter(lookup_expr="icontains")
    homeworld = CharFilter(lookup_expr="icontains")

    eye_color = CharFilter(lookup_expr="icontains")
    hair_color = CharFilter(lookup_expr="icontains")
    gender = CharFilter(lookup_expr="icontains")

    _class = CharFilter(
        field_name="attributes__class",
        lookup_expr="icontains",
        label="Class",
    )
    born_location = CharFilter(
        field_name="attributes__born_location",
        lookup_expr="icontains",
        label="Born Location",
    )
    plating_color = CharFilter(
        field_name="attributes__plating_color",
        lookup_expr="icontains",
        label="Plating Color",
    )
    cybernetics = CharFilter(
        field_name="attributes__cybernetics",
        lookup_expr="icontains",
        label="Cybernetics",
    )
    manufacturer = CharFilter(
        field_name="attributes__manufacturer",
        lookup_expr="icontains",
        label="Manufacturer",
    )
    model = CharFilter(
        field_name="attributes__model",
        lookup_expr="icontains",
        label="Model",
    )
    sensor_color = CharFilter(
        field_name="attributes__sensor_color",
        lookup_expr="icontains",
        label="Sensor Color",
    )
    equipment = CharFilter(
        field_name="attributes__equipment",
        lookup_expr="icontains",
        label="Equipment",
    )
    era = CharFilter(
        field_name="attributes__era",
        lookup_expr="icontains",
        label="Era",
    )
    date_destroyed = CharFilter(
        field_name="attributes__date_destroyed",
        lookup_expr="icontains",
        label="Date Destroyed",
    )
    destroyed_location = CharFilter(
        field_name="attributes__destroyed_location",
        lookup_expr="icontains",
        label="Destroyed Location",
    )
    product_line = CharFilter(
        field_name="attributes__product_line",
        lookup_expr="icontains",
        label="Product Line",
    )
    armament = CharFilter(
        field_name="attributes__armament",
        lookup_expr="icontains",
        label="Armament",
    )
    creator = CharFilter(
        field_name="attributes__creator",
        lookup_expr="icontains",
        label="Creator",
    )
    kajidic = CharFilter(
        field_name="attributes__kajidic",
        lookup_expr="icontains",
        label="Kajidic",
    )
    degree = CharFilter(
        field_name="attributes__degree",
        lookup_expr="icontains",
        label="Degree",
    )
    date_created = CharFilter(
        field_name="attributes__date_created",
        lookup_expr="icontains",
        label="Date Created",
    )

    class Meta:
        model = Character
        fields = {
            "born": ["exact", "gte", "lte"],
            "died": ["exact", "gte", "lte"],

        }
