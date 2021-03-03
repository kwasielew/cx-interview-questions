from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


class BaseCatalogueProvider(ABC):
    @abstractmethod
    def get_price(self, sku: str) -> Decimal:
        ...


@dataclass
class CatalogueProvider(BaseCatalogueProvider):
    """ Catalogues provider which stores SKU-price mapping in dictionary """
    sku_price: Dict[str, Decimal]

    def get_price(self, sku: str) -> Decimal:
        return self.sku_price.get(sku, Decimal("0"))
