# Documentation

## Virtual environment setup

Create new virtual env
```bash
virtualenv -p python3.8.5 venv
```

Activate virtual env
```bash
. venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Script with few examples

In `demo_script.py` there a few example baskets implemented. 
It provides basic info how to use this library. 

## Unit tests

In order to run unit tests simply type:

```bash
pytest
```

## How to use BasketPricer

`BasketPricer` class requires two objects on it's creation:

- `catalogue_provider`, which is responsible for retrieving the price of the product from the catalog.
 This library comes with `CatalogueProvider` class which basically stores SKU:price relationship in a dictionary.
 NOTE: if it doesn't find product with specified SKU it returns zero.
If there is a need to get product price from a database or API, you can do so by creating your own catalogue provider
 by subclassing `BaseCatalogueProvider`.
You have to adapt to the interface of `get_price(sku)` method, which accepts SKU parameter and returns price.
 

- `offer_provider`, responsible for collecting offers for a given product. Similarly to catalogue provider there
is `OfferProvider` available out of the box, which stores SKU-offers mapping in dictionary.
To write your own offer provider inherit from `BaseOfferProvider` abstract class. The only required method is 
`get_offers` which requires `sku` as a parameter and returns a list of offers.


### Calculating prices

Instance of `BasketPricer` has single 'public' method - `calculate_basket_prices`. 
It accepts basket parameter in form of primitive data structure dictionary, where keys are SKUs and values are quantities.

First it fetches price and offers for every product in the basket (only). There is no need to pass whole catalogue and 
all offers to the constructor.

Next it calculates subtotal and discount for every product in the basket.

At the end it sums up prices and returns them as a dictionary.


### Offers

The library comes with two ready to use offers:

- `PercentageOffer` - calculates discount based on passed percentage in the constructor. 
- `EveryXIsFreeOffer` - gives next product free if X were bought.

In order to create custom offer inherit from `BaseOffer` abstract class.
`calculate_discount` method is mandatory and it accepts `price` and `quantity` as parameters.
  