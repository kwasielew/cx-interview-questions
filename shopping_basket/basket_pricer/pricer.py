from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from basket_pricer.interfaces import BaseCatalogueProvider
from shopping_basket_tests.exceptions import NegativeBasketPriceException


@dataclass
class BasketPricer:
    catalogue_provider: BaseCatalogueProvider

    def _calculate_sub_total(self, basket: Dict[str, int]):
        sub_total = Decimal('0')
        for sku, quantity in basket.items():
            sub_total += self.catalogue_provider.get_price(sku) * quantity

        if sub_total < Decimal('0'):
            raise NegativeBasketPriceException
        return sub_total

    def calculate_basket_prices(self, basket: Dict[str, int]):
        """
        Return sub total, discount and total prices.
        Basket param is a dictionary where keys are product SKUs and values are quantities in the basket.
        """
        return {
            'sub_total': self._calculate_sub_total(basket),
            'discount': Decimal('0'),
            'total': Decimal('0')
        }
