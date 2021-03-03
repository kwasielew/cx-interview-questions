from basket_pricer.interfaces import BaseCatalogueProvider
from basket_pricer.pricer import BasketPricer


class FakeCatalogueProvider(BaseCatalogueProvider):
    pass


def test_create_basket_pricer_with_catalogue_provider():
    catalogue_provider = FakeCatalogueProvider()
    BasketPricer(catalogue_provider)
