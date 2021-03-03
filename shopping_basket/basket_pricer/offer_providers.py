from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

from basket_pricer.offers import BaseOffer


class BaseOfferProvider(ABC):
    @abstractmethod
    def get_offers(self, sku: str) -> List[BaseOffer]:
        ...


@dataclass
class OfferProvider(BaseOfferProvider):
    """ Offers provider based on dictionary with SKU-list of offers mapping """
    sku_offers: Dict[str, List[BaseOffer]]

    def get_offers(self, sku: str) -> List[BaseOffer]:
        return self.sku_offers.get(sku, [])
