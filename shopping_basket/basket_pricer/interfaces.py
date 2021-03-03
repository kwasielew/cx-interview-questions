from abc import ABC, abstractmethod
from decimal import Decimal


class BaseCatalogueProvider(ABC):
    @abstractmethod
    def get_price(self, sku: str) -> Decimal: ...
