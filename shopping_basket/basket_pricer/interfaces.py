from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List

from basket_pricer.offers import BaseOffer


class BaseCatalogueProvider(ABC):
    @abstractmethod
    def get_price(self, sku: str) -> Decimal:
        ...


class BaseOfferProvider(ABC):
    @abstractmethod
    def get_offers(self, sku: str) -> List[BaseOffer]:
        ...
