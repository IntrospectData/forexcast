# Forexcast

Simple currency forecasting for IEX data

## Installation

### Using pip

`$ pip3 install forexcast`

### From source

`$ git clone git@github.com:IntrospectData/forexcast.git`

`$ python3 -m venv env`

`$ source env/bin/activate`

`(env) $ pip3 install forexcast`


## Setup
On your first use the app will ask for your IEX api key and your desired quote-currency.

These values are stored *unencrypted* in `$HOME/.config/forexcast.json`

## Usage
```bash
$ forexcast --help
Usage: forexcast [OPTIONS] CURRENCY

  Simple currency forecasting for IEX data

  * CURRENCY = 3 char ISO code for target currency

  * Dates should be in YYYY-MM-DD format

Options:
  --from_date TEXT   Data after this date will be included.
  --to_date TEXT     Data after this date will be excluded.
  --periods INTEGER  Periods to predict.
  --out TEXT         If specified will save forecast in specified dir.
  --help             Show this message and exit.
```
