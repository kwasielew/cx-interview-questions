from decimal import Decimal

from basket_pricer.catalogues_providers import CatalogueProvider
from basket_pricer.offer_providers import OfferProvider
from basket_pricer.offers import EveryXIsFreeOffer, PercentageOffer
from basket_pricer.pricer import BasketPricer

CATALOGUE = CatalogueProvider(
    {
        "Baked Beans": Decimal("0.99"),
        "Biscuits": Decimal("1.20"),
        "Sardines": Decimal("1.89"),
        "Shampoo (Small)": Decimal("2.00"),
        "Shampoo (Medium)": Decimal("2.50"),
        "Shampoo (Large)": Decimal("3.50"),
    }
)

OFFERS = OfferProvider(
    {
        "Baked Beans": [EveryXIsFreeOffer(2)],
        "Sardines": [PercentageOffer(Decimal("25"))],
    }
)


def print_prices(prices):
    """
    Helper function to print results of calculations.
    """
    print("Basket result prices:")
    print(f'Sub Total: £{prices["sub_total"]}')
    print(f'Discount: £{prices["discount"]}')
    print(f'Total: £{prices["total"]}')


def demonstrate_basket_1():
    """
    Basket 1 from examples.
    """
    print("BASKET 1 DEMO:")
    basket = {"Baked Beans": 4, "Biscuits": 1}
    pricer = BasketPricer(CATALOGUE, OFFERS)
    print_prices(pricer.calculate_basket_prices(basket))


def demonstrate_basket_2():
    """
    Basket 2 from examples.
    """
    print("\n\n\nBASKET 2 DEMO:")
    basket = {"Baked Beans": 2, "Biscuits": 1, "Sardines": 2}
    pricer = BasketPricer(CATALOGUE, OFFERS)
    print_prices(pricer.calculate_basket_prices(basket))


def demonstrate_basket_3():
    """
    Nine for the price of six example.
    """
    print("\n\n\nBASKET 3 DEMO:")
    basket = {"Baked Beans": 9}
    pricer = BasketPricer(CATALOGUE, OFFERS)
    print_prices(pricer.calculate_basket_prices(basket))


if __name__ == "__main__":
    demonstrate_basket_1()
    demonstrate_basket_2()
    demonstrate_basket_3()
