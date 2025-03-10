from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import CharacterFilter
from .models import Affiliation, Character, Team, TeamMembership
from .serializers import (
    AffiliationListSerializer,
    CharacterDetailSerializer,
    CharacterListSerializer,
    TeamMembershipSerializer,
    TeamSerializer,
)


class AffiliationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns a list of affiliations.
    """
    serializer_class = AffiliationListSerializer
    queryset = Affiliation.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("characters")
        return qs


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only endpoint for characters.
    """
    filterset_class = CharacterFilter
    queryset = Character.objects.none()

    @action(detail=False, methods=["get"])
    def attribute_list(self, request):
        """
        Returns a list of possible attributes for a character.
        """
        attributes = set(
            [
                key
                for attributes in Character.objects.values_list(
                    "attributes", flat=True)
                for key in attributes
            ]
        )
        return Response(attributes)

    def list_for_team(self, request, team_pk=None):
        """
        Returns a list of characters for a team.
        """
        qs = self.get_queryset().filter(teams=team_pk)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CharacterDetailSerializer
        return CharacterListSerializer

    def get_queryset(self):
        qs = Character.objects.filter(is_placeholder=False)
        # Prefetch related fields to reduce the number of queries
        qs.prefetch_related(
            "affiliations", "teams", "former_affiliations",
            "master", "apprentices")
        return qs


class TeamMemberShipViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    Returns a list of team memberships.
    """
    serializer_class = TeamMembershipSerializer
    queryset = TeamMembership.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("team", "character")
        return qs


class TeamMembershipDeleteView(generics.DestroyAPIView):
    """
    Deletes a team membership.
    """

    def destroy(self, request, team_pk=None, character_pk=None):
        """
        Deletes a team membership.
        """
        obj = get_object_or_404(
            TeamMembership.objects.all(),
            team_id=team_pk,
            character_id=character_pk
        )
        obj.delete()

        return Response(status=204)

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)

        return obj


class TeamViewSet(viewsets.ModelViewSet):
    """
    Returns a list of teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("members")
        return qs
