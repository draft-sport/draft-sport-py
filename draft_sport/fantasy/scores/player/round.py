"""
Draft Sport Python
Player Round Points Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.scores.player.score import Score
from typing import List, TypeVar, Type, Any
from nozomi import Decodable

T = TypeVar('T', bound='Round')


class Round(Decodable):
    """Points attributed to a player in a particular round"""

    def __init__(
        self,
        sequence: int,
        points: List[Score]
    ) -> None:

        self._round_sequence = sequence
        self._points = points

        return

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            sequence=data['round_sequence'],
            points=Score.decode_many(data['scores'])
        )
