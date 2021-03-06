"""
Draft Sport Python
Fantasy Player Score Module
Author: hugh@blinkybeach.com
"""
from nozomi import Decodable, HTTPMethod, URLParameter, URLParameters
from nozomi import Immutable, ApiRequest, RequestCredentials, Encodable
from draft_sport.fantasy.player.profile import Profile
from draft_sport.fantasy.season.season import Season
from typing import Type, TypeVar, Any, Optional, List
from draft_sport.ancillary.configuration import Configuration
from draft_sport.fantasy.scores.player.order_by import OrderBy
from draft_sport.fantasy.scores.player.points import Points
from draft_sport.universe.position.category import PositionCategory
from draft_sport.data.order import Order
from typing import Dict

T = TypeVar('T', bound='Player')


class ScoreCard(Decodable, Encodable):

    _PATH = '/fantasy/score-card'
    _LIST_PATH = '/fantasy/score-card/list'

    def __init__(
        self,
        profile: Profile,
        season_id: str,
        limit: int,
        offset: int,
        query_count: int,
        sequence: int,
        requesting_agent_id: str,
        points: Points,
        query_time: int
    ) -> None:

        self._profile = profile
        self._season_id = season_id
        self._limit = limit
        self._offset = offset
        self._query_count = query_count
        self._sequence = sequence
        self._requesting_agent_id = requesting_agent_id
        self._points = points
        self._query_time = query_time

        return

    public_id = Immutable(lambda s: s._profile.public_id)

    profile = Immutable(lambda s: s._profile)
    season_id = Immutable(lambda s: s._season_id)
    limit = Immutable(lambda s: s._limit)
    offset = Immutable(lambda s: s._offset)
    query_count = Immutable(lambda s: s._query_count)
    sequence = Immutable(lambda s: s._sequence)
    requesting_agent_id = Immutable(lambda s: s._requesting_agent_id)
    points = Immutable(lambda s: s._points)
    query_time = Immutable(lambda s: s._query_time)

    query_time_seconds = Immutable(
        lambda s: str(int(s._query_time) / 1000000)
    )

    def has_position_with_name(self, name: str) -> bool:
        """Return True if this Player has the named position"""
        return self._profile.position_name == name

    def has_position_in_category(self, category: PositionCategory) -> bool:
        """Return True if this Player has a position in the supplied category"""
        return category in self._profile.position.categories

    def encode(self) -> Dict[str, Any]:
        return {
            'player': self._profile.encode(),
            'limit': self._limit,
            'offset': self._offset,
            'sequence': self._sequence,
            'requesting_agent_id': self._requesting_agent_id,
            'points': self._points.encode(),
            'query_time': self._query_time,
            'query_count': self._query_coun
        }

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            profile=Profile.decode(data['player']),
            season_id=data['fantasy_season_id'],
            limit=data['limit'],
            offset=data['offset'],
            query_count=data['query_count'],
            sequence=data['sequence'],
            requesting_agent_id=data['requesting_agent_id'],
            points=Points.decode(data['points']),
            query_time=data['query_time']
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        public_id: str,
        season: Season,
        credentials: Optional[RequestCredentials],
        configuration: Optional[Configuration]
    ) -> Optional[T]:

        parameters = URLParameters([
            URLParameter('public_id', public_id),
            URLParameter('season', season.public_id)
        ])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            data=None,
            url_parameters=parameters,
            credentials=credentials,
            configuration=configuration
        )

        return cls.optionally_decode(request.response_data)

    @classmethod
    def retrieve_many(
        cls: Type[T],
        season: Season,
        offset: int,
        limit: int,
        configuration: Configuration,
        order_by: OrderBy = OrderBy.TOTAL_SEASON_POINTS,
        order: Order = Order.DESCENDING,
        name_fragment: Optional[str] = None,
        credentials: Optional[RequestCredentials] = None
    ) -> List[T]:

        parameters = URLParameters([
            URLParameter('season', season.public_id),
            URLParameter('offset', offset),
            URLParameter('limit', limit),
            URLParameter('order_by', order_by.value),
            URLParameter('order', order.value)
        ])

        if name_fragment is not None:
            parameters.append(URLParameter('fragment', name_fragment))

        request = ApiRequest(
            path=cls._LIST_PATH,
            method=HTTPMethod.GET,
            data=None,
            url_parameters=parameters,
            credentials=credentials,
            configuration=configuration
        )

        return cls.optionally_decode_many(
            request.response_data,
            default_to_empty_list=True
        )
