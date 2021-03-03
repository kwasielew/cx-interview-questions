from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

import pytest

from basket_pricer.interfaces import BaseCatalogueProvider, BaseOfferProvider, BaseOffer
from basket_pricer.pricer import BasketPricer
from shopping_basket_tests.exceptions import NegativeBasketPriceException


@dataclass
class FakeCatalogueProvider(BaseCatalogueProvider):
    catalogue: Dict[str, Decimal]

    def get_price(self, sku: str) -> Decimal:
        return self.catalogue.get(sku, Decimal('0'))


@dataclass
class FakeOfferProvider(BaseOfferProvider):
    offers: Dict[str, List[BaseOffer]]

    def get_offers(self, sku: str) -> List[BaseOffer]:
        return self.offers.get(sku)


@dataclass
class PercentageOffer(BaseOffer):
    discount_percent: Decimal

    def calculate_discount(self, price: Decimal) -> Decimal:
        return (price * self.discount_percent) / 100


def test_pricer_returns_prices():
    catalogue_provider = FakeCatalogueProvider({})
    offer_provider = FakeOfferProvider({})
    basket = {}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    assert pricer.calculate_basket_prices(basket) == {
        'sub_total': Decimal('0'),
        'discount': Decimal('0'),
        'total': Decimal('0')
    }


@pytest.mark.skip('In progress')
def test_pricer_calculates_sub_total_from_basket_products():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('5')})
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    assert pricer.calculate_basket_prices(basket) == {
        'sub_total': Decimal('5'),
        'discount': Decimal('0'),
        'total': Decimal('5')
    }


def test_pricer_returns_raises_exception_when_product_is_not_in_catalogue():
    catalogue_provider = FakeCatalogueProvider({})
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 2}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    assert pricer.calculate_basket_prices(basket) == {
        'sub_total': Decimal('0'),
        'discount': Decimal('0'),
        'total': Decimal('0')
    }


def test_pricer_returns_zero_prices_when_basket_is_empty():
    catalogue_provider = FakeCatalogueProvider(
        {
            'APPLE': Decimal('5'),
            'CHEESE': Decimal('3')
        }
    )
    offer_provider = FakeOfferProvider({})
    basket = {}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    assert pricer.calculate_basket_prices(basket) == {
        'sub_total': Decimal('0'),
        'discount': Decimal('0'),
        'total': Decimal('0')
    }


def test_pricer_calculates_sub_total_using_product_price():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('5')})
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    prices = pricer.calculate_basket_prices(basket)
    assert prices['sub_total'] == Decimal('5')


def test_pricer_calculates_sub_total_for_multi_quantity():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('5')})
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 3}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    prices = pricer.calculate_basket_prices(basket)
    assert prices['sub_total'] == Decimal('15')


def test_pricer_calculates_sub_total_for_multiple_products_in_basket():
    catalogue_provider = FakeCatalogueProvider(
        {
            'APPLE': Decimal('5'),
            'CHEESE': Decimal('3')
        }
    )
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 2, 'CHEESE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    prices = pricer.calculate_basket_prices(basket)
    assert prices['sub_total'] == Decimal('13')


# TODO: handle case when discount is bigger than sub total
def test_pricer_calculated_sub_total_cant_be_negative():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('-5')})
    offer_provider = FakeOfferProvider({})
    basket = {'APPLE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    with pytest.raises(NegativeBasketPriceException):
        pricer.calculate_basket_prices(basket)


def test_pricer_calculates_percentage_discount_for_product():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('5')})
    offer_provider = FakeOfferProvider({'APPLE': [PercentageOffer(Decimal('10'))]})
    basket = {'APPLE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    prices = pricer.calculate_basket_prices(basket)
    assert prices['discount'] == Decimal('0.5')


def test_pricer_calculates_chooses_highest_discount():
    catalogue_provider = FakeCatalogueProvider({'APPLE': Decimal('5')})
    offer_provider = FakeOfferProvider(
        {
            'APPLE': [PercentageOffer(Decimal('10')), PercentageOffer(Decimal('15'))],
        }
    )
    basket = {'APPLE': 1}
    pricer = BasketPricer(catalogue_provider, offer_provider)
    prices = pricer.calculate_basket_prices(basket)
    assert prices['discount'] == Decimal('0.75')
