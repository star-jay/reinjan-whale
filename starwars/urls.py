from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from starwars.characters.views import (
    AffiliationViewSet,
    CharacterViewSet,
    TeamMembershipDeleteView,
    TeamMemberShipViewSet,
    TeamViewSet,
)

router = DefaultRouter()

router.register('affiliations', AffiliationViewSet, basename='affiliation')
router.register('characters', CharacterViewSet, basename='character')
router.register('teams', TeamViewSet, basename='team')
router.register(
    'team-memberships', TeamMemberShipViewSet, basename='teammembership')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the router URLs
    path('', include(router.urls)),
    # Allow login/logout to browseable DRF views:
    path('auth/', include('rest_framework.urls')),

    # Add bidirectional links to the characters in both directions
    path(
        'teams/<int:team_pk>/members/',
        CharacterViewSet.as_view({'get': 'list_for_team'}),
        name='team-characters'
    ),
    path(
        'characters/<int:team_pk>/members/',
        TeamViewSet.as_view({'get': 'list_for_character'}),
        name='character-teams'
    ),

    # delete team memberships in both directions
    path(
        'teams/<int:team_pk>/members/<int:character_pk>/',
        TeamMembershipDeleteView.as_view(),
        name='team-member'
    ),
    path(
        'characters/<int:character_pk>/teams/<int:team_pk>/',
        TeamMembershipDeleteView.as_view(),
        name='team-member'
    ),

]
