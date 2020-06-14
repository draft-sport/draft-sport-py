"""
Draft Sport
Team Module
author: hugh@blinkybeach.com
"""
from typing import List, Any, TypeVar, Type, Optional
from nozomi import Immutable, Decodable, RequestCredentials, ApiRequest
from nozomi import Configuration, URLParameter, URLParameters, HTTPMethod
from draft_sport.leagues.composition import Composition
from draft_sport.leagues.pick import Pick
from draft_sport.leagues.filled_composition import FilledComposition
from draft_sport.leagues.filled_requirement import FilledRequirement

T = TypeVar('T', bound='Team')


class Team(Decodable):

    _PATH = '/league/team'

    def __init__(
        self,
        league_id: str,
        picks: List[Pick],
        manager_id: str,
        manager_display_name: str,
        name: Optional[str],
        total_points: int,
        composition: Composition
    ) -> None:

        self._league_id = league_id
        self._picks = picks
        self._manager_id = manager_id
        self._manager_display_name = manager_display_name
        self._name = name
        self._total_points = total_points
        self._composition = composition

        return

    league_id = Immutable(lambda s: s._league_id)
    picks = Immutable(lambda s: s._picks)
    manager_id = Immutable(lambda s: s._manager_id)
    manager_display_name = Immutable(lambda s: s._manager_display_name)
    name = Immutable(lambda s: s._name)
    total_points = Immutable(lambda s: s._total_points)

    filled_composition = Immutable(
        lambda s: s._compute_filled_composition()
    )

    def _compute_filled_composition(self) -> FilledComposition:

        filled_requirements: List[FilledRequirement] = list()

        remaining_picks = list(self._picks)

        for requirement in self._composition.position_requirements:

            picks_satisfying_requirement: List[Pick] = list()

            for pick in remaining_picks:
                from draft_sport.fantasy.scores.player.score_card import ScoreCard
                print(type(pick.score_card))
                assert isinstance(pick.score_card, ScoreCard)
                if pick.score_card.has_position_with_name(
                    name=requirement.position_name
                ):
                    picks_satisfying_requirement.append(pick)
                    remaining_picks.remove(pick)

                continue

            filled_requirements.append(FilledRequirement(
                requirement=requirement,
                picks=picks_satisfying_requirement
            ))

            continue

        for category_requirement in self._composition.category_requirements:

            picks_satisfying_requirement: List[Pick] = list()

            for pick in remaining_picks:
                if pick.score_card.has_position_in_category(
                    category=category_requirement.category
                ):
                    picks_satisfying_requirement.append(pick)
                    remaining_picks.remove(pick)

                continue

            filled_requirements.append(FilledRequirement(
                requirement=category_requirement,
                picks=picks_satisfying_requirement
            ))

            continue

        return FilledComposition(requirements=filled_requirements)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            league_id=data['league_id'],
            picks=Pick.decode_many(data['picks']),
            manager_id=data['manager_id'],
            manager_display_name=data['manager_display_name'],
            name=data['name'],
            total_points=data['total_points'],
            composition=Composition.decode(data['composition'])
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        league_id: str,
        manager_id: str,
        credentials: RequestCredentials,
        configuration: Configuration
    ) -> Optional[T]:
        """
        Return a Team in the supplied League, managed by the supplied Manager,
        if it exists.
        """

        parameters = URLParameters([
            URLParameter('league', league_id),
            URLParameter('manager', manager_id)
        ])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            configuration=configuration,
            data=None,
            url_parameters=parameters,
            credentials=credentials
        )

        return cls.optionally_decode(request.response_data)
