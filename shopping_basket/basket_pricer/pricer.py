from dataclasses import dataclass

from basket_pricer.interfaces import BaseCatalogueProvider


@dataclass
class BasketPricer:
    catalogue_provider: BaseCatalogueProvider
