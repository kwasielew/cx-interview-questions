from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List


class BaseCatalogueProvider(ABC):
    @abstractmethod
    def get_price(self, sku: str) -> Decimal:
        ...


class BaseOffer(ABC):
    @abstractmethod
    def calculate_discount(self, price: Decimal, quantity: int) -> Decimal:
        ...


class BaseOfferProvider(ABC):
    @abstractmethod
    def get_offers(self, sku: str) -> List[BaseOffer]:
        ...
