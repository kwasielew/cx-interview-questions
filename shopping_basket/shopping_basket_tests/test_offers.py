from decimal import Decimal

import pytest

from basket_pricer.exceptions import OfferConfigurationException
from basket_pricer.offers import EveryXIsFreeOffer, PercentageOffer


def test_percentage_offer_calculates_discount():
    offer = PercentageOffer(Decimal("10"))
    price = Decimal("5")
    quantity = 1
    assert offer.calculate_discount(price, quantity) == Decimal("0.5")


def test_percentage_offer_calculates_discount_with_100_percents():
    offer = PercentageOffer(Decimal("100"))
    price = Decimal("5")
    quantity = 1
    assert offer.calculate_discount(price, quantity) == Decimal("5")


def test_percentage_offer_calculates_discount_with_multiple_items():
    offer = PercentageOffer(Decimal("10"))
    price = Decimal("5")
    quantity = 3
    assert offer.calculate_discount(price, quantity) == Decimal("1.5")


def test_percentage_offer_raises_when_discount_percentage_is_negative():
    offer = PercentageOffer(Decimal("-3"))
    price = Decimal("5")
    quantity = 1
    with pytest.raises(OfferConfigurationException) as excinfo:
        offer.calculate_discount(price, quantity)

    assert "Discount percentage cannot be negative" == str(excinfo.value)


def test_percentage_offer_raises_when_discount_percentage_is_higher_than_100_percents():
    offer = PercentageOffer(Decimal("101"))
    price = Decimal("5")
    quantity = 1
    with pytest.raises(OfferConfigurationException) as excinfo:
        offer.calculate_discount(price, quantity)

    assert "Discount percentage cannot be higher than 100%" == str(excinfo.value)


def test_every_x_bought_product_free_offer_calculates_discount():
    offer = EveryXIsFreeOffer(2)
    price = Decimal("5")
    quantity = 3
    assert offer.calculate_discount(price, quantity) == Decimal("5")


def test_every_x_bought_product_free_offer_calculates_discount_with_multiple_items():
    offer = EveryXIsFreeOffer(2)
    price = Decimal("5")
    quantity = 8
    assert offer.calculate_discount(price, quantity) == Decimal("10")


def test_every_x_bought_product_free_offer_calculates_discount_zero():
    offer = EveryXIsFreeOffer(2)
    price = Decimal("5")
    quantity = 0
    assert offer.calculate_discount(price, quantity) == Decimal("0")


def test_first_is_free():
    offer = EveryXIsFreeOffer(0)
    price = Decimal("5")
    quantity = 1
    assert offer.calculate_discount(price, quantity) == Decimal("5")


def test_every_x_bought_product_free_offer_raises_exception_when_free_after_value_is_below_zero():
    offer = EveryXIsFreeOffer(-1)
    price = Decimal("5")
    quantity = 1
    with pytest.raises(OfferConfigurationException) as excinfo:
        offer.calculate_discount(price, quantity)

    assert "One free after X bought value cannot be negative" == str(excinfo.value)
