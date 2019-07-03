from models.rate import Rate
from typing import Iterable


class Currency:
    def __init__(self, name: str, rates: Iterable[Rate]):
        self.name = name
        self.rates = rates
