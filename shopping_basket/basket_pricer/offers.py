from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from basket_pricer.exceptions import OfferConfigurationException


class BaseOffer(ABC):
    @abstractmethod
    def calculate_discount(self, price: Decimal, quantity: int) -> Decimal:
        ...


@dataclass
class PercentageOffer(BaseOffer):
    """ Offer which calculates percentage discount """

    discount_percent: Decimal

    def calculate_discount(self, price: Decimal, quantity: int) -> Decimal:
        if self.discount_percent < Decimal("0"):
            raise OfferConfigurationException("Discount percentage cannot be negative")
        if self.discount_percent > Decimal("100"):
            raise OfferConfigurationException(
                "Discount percentage cannot be higher than 100%"
            )

        return (price * quantity * self.discount_percent) / 100


@dataclass
class EveryXIsFreeOffer(BaseOffer):
    """ Offer where after buying X product items next is free """

    one_free_after: int

    def calculate_discount(self, price: Decimal, quantity: int) -> Decimal:
        if self.one_free_after < 0:
            raise OfferConfigurationException(
                "One free after X bought value cannot be negative"
            )
        number_of_free_products = quantity // (self.one_free_after + 1)
        return number_of_free_products * price
