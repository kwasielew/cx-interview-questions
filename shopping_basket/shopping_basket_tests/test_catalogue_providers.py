from decimal import Decimal

from basket_pricer.catalogues_providers import CatalogueProvider


def test_catalogue_provider_gets_price_for_sku():
    provider = CatalogueProvider({'PAN': Decimal('2')})
    assert provider.get_price('PAN') == Decimal('2')


def test_catalogue_provider_returns_zero_when_no_sku():
    provider = CatalogueProvider({})
    assert provider.get_price('PAN') == Decimal('0')
