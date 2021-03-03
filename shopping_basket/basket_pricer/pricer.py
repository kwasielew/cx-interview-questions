from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

from basket_pricer.interfaces import BaseCatalogueProvider, BaseOfferProvider
from shopping_basket_tests.exceptions import NegativeBasketPriceException


@dataclass
class BasketPricer:
    catalogue_provider: BaseCatalogueProvider
    offer_provider: BaseOfferProvider

    def _prepare_basket_items(self, basket: Dict[str, int]) -> List[Dict]:
        return [
            {
                'sku': sku,
                'quantity': quantity,
                'price': self.catalogue_provider.get_price(sku),
                'offers': self.offer_provider.get_offers(sku)
            } for sku, quantity in basket.items()
        ]

    @staticmethod
    def _calculate_prices_for_basket_item(basket_item: Dict) -> Dict[str, Decimal]:
        discount = Decimal('0')
        for offer in basket_item.get('offers') or []:
            discount = max(discount, offer.calculate_discount(basket_item.get('price')))

        return {
            'sku': basket_item.get('sku'),
            'sub_total': basket_item.get('price') * basket_item.get('quantity'),
            'discount': discount
        }

    @staticmethod
    def _calculate_overal_sub_total(basket_items_prices: List[Dict]) -> Decimal:
        sub_total = sum(item.get('sub_total') for item in basket_items_prices)
        if sub_total < Decimal('0'):
            raise NegativeBasketPriceException
        return sub_total

    @staticmethod
    def _calculate_overal_discount(basket_items_prices: List[Dict]) -> Decimal:
        return sum((item.get('discount') for item in basket_items_prices))

    def calculate_basket_prices(self, basket: Dict[str, int]):
        """
        Return sub total, discount and total prices.
        Basket param is a dictionary where keys are product SKUs and values are quantities in the basket.
        """
        basket_items = self._prepare_basket_items(basket)
        calculated_basket_items_prices = [self._calculate_prices_for_basket_item(item) for item in basket_items]

        return {
            'sub_total': self._calculate_overal_sub_total(calculated_basket_items_prices),
            'discount': self._calculate_overal_discount(calculated_basket_items_prices),
            'total': Decimal('0')
        }
