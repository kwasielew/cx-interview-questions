from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

from basket_pricer.exceptions import NegativeBasketPriceException
from basket_pricer.catalogues_providers import BaseCatalogueProvider
from basket_pricer.offer_providers import BaseOfferProvider


@dataclass
class BasketPricer:
    catalogue_provider: BaseCatalogueProvider
    offer_provider: BaseOfferProvider

    def _prepare_basket_items(self, basket: Dict[str, int]) -> List[Dict]:
        return [
            {
                "sku": sku,
                "quantity": quantity,
                "price": self.catalogue_provider.get_price(sku),
                "offers": self.offer_provider.get_offers(sku),
            }
            for sku, quantity in basket.items()
        ]

    @staticmethod
    def _calculate_prices_for_basket_item(basket_item: Dict) -> Dict[str, Decimal]:
        discount = Decimal("0")
        for offer in basket_item.get("offers"):
            discount = max(
                discount,
                offer.calculate_discount(
                    basket_item.get("price"), basket_item.get("quantity")
                ),
            )

        return {
            "sub_total": basket_item.get("price") * basket_item.get("quantity"),
            "discount": discount,
        }

    @staticmethod
    def _calculate_overall_sub_total(basket_items_prices: List[Dict]) -> Decimal:
        sub_total = sum(
            item.get("sub_total") for item in basket_items_prices
        ) or Decimal("0")
        return sub_total.quantize(Decimal(".00"), rounding=ROUND_HALF_UP)

    @staticmethod
    def _calculate_overall_discount(basket_items_prices: List[Dict]) -> Decimal:
        discount = sum(item.get("discount") for item in basket_items_prices) or Decimal(
            "0"
        )
        return discount.quantize(Decimal(".00"), rounding=ROUND_HALF_UP)

    def calculate_basket_prices(self, basket: Dict[str, int]) -> Dict[str, Decimal]:
        """
        Basket param is a dictionary where keys are product SKUs and values are quantities in the basket.
        Return sub total, discount and total prices.
        """
        basket_items = self._prepare_basket_items(basket)
        calculated_basket_items_prices = [
            self._calculate_prices_for_basket_item(item) for item in basket_items
        ]

        sub_total = self._calculate_overall_sub_total(calculated_basket_items_prices)
        discount = self._calculate_overall_discount(calculated_basket_items_prices)
        total = sub_total - discount
        if total < Decimal("0"):
            raise NegativeBasketPriceException

        return {"sub_total": sub_total, "discount": discount, "total": total}
