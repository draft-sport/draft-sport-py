"""
Draft Sport Python Library
Offer Module
author: hugh@blinkybeach.com
"""
from typing import TypeVar, Type, Any, List, Optional
from nozomi import Decodable
from draft_sport.store.price import Price
from draft_sport.store.product import Product
from nozomi import Immutable, Configuration, RequestCredentials
from nozomi import URLParameter, URLParameters, HTTPMethod, ApiRequest

T = TypeVar('T', bound='Offer')


class Offer(Decodable):

    def __init___(
        self,
        public_id: str,
        name: str,
        prices: List[Price],
        products: List[Product]
    ) -> None:

        self._public_id = public_id
        self._name = name
        self._prices = prices
        self._products = products

        return

    public_id: str = Immutable(lambda s: s._public_id)
    name: str = Immutable(lambda s: s._name)
    prices: List[Price] = Immutable(lambda s: s._prices)
    products: List[Product] = Immutable(lambda s: s._products)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            name=data['name'],
            prices=Price.decode_many(data['prices']),
            products=Product.decode_many(data['products'])
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        public_id: str,
        credentials: RequestCredentials,
        configuration: Configuration
    ) -> Optional[T]:

        parameters = URLParameters([URLParameter('offer', public_id)])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            configuration=configuration,
            data=None,
            url_parameters=parameters,
            credentials=credentials
        )

        return cls.optionally_decode(request.response_data)
