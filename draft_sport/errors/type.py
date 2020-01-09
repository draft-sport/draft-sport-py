"""
Draft Sport
TypeError Module
author: hugh@blinkybeach.com
"""
from draft_sport.errors.error import DraftSportError
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='DSTypeError')


class DSTypeError(DraftSportError):

    _TEMPLATE = '`{n}` must be of type `{t}`, got `{g}`'

    def __init__(
        self,
        variable: Any,
        variable_name: str,
        expected_type: Type
    ) -> None:

        description = self._TEMPLATE.format(
            n=variable_name,
            t=str(expected_type),
            g=str(type(variable))
        )

        super().__init__(description)

    @classmethod
    def assert_type(
        cls: Type[T],
        variable: Any,
        variable_name: str,
        expected_type: Type
    ) -> None:

        if type(variable) != expected_type:
            raise cls(
                variable=variable,
                variable_name=variable_name,
                expected_type=expected_type
            )

        return
