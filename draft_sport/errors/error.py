"""
Draft Sport
Error Module
author: hugh@blinkybeach.com
"""


class DraftSportError(Exception):

    def __init__(self, description: str) -> None:

        self._description = description
        super().__init__(self)
        return
