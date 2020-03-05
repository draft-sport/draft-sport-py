"""
Draft Sport Python Library
Challenge Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Configuration, RequestCredentials
from nozomi import Decodable, NozomiTime
from typing import TypeVar, Type, Any, Optional
from nozomi import URLParameter, URLParameters, HTTPMethod, ApiRequest

T = TypeVar('T', bound='Challenge')


class Challenge(Decodable):

    _PATH = '/communication-method/challenge'

    def __init__(
        self,
        expiration: NozomiTime,
        completed: Optional[NozomiTime],
        is_expired: bool,
    ) -> None:

        self._expiration = expiration
        self._is_expired = is_expired
        self._completed = completed

        return

    is_completed = Immutable(lambda s: s._completed is not None)
    is_expired = Immutable(lambda s: s._is_expired)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            expiration=NozomiTime.decode(data['expiration']),
            completed=NozomiTime.optionally_decode(data['completed']),
            is_expired=data['is_expired']
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        code: str,
        credentials: RequestCredentials,
        configuration: Configuration
    ) -> Optional[T]:

        parameters = URLParameters([
            URLParameter('code', code)
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
