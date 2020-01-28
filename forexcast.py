import datetime
import json
import os

import click
import requests

import pandas as pd
import plotly.offline as ply
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

default_config = {
    "apikey": "-",
    "quote_currency": "USD",
}

APIKEY = ''
QUOTE_CURRENCY = ''
HOME = os.getenv("HOME")

def _config():
    apikey = input("Enter your IEX api key: ")
    quote_currency = input("Enter quote currency: ")
    if apikey and quote_currency:
        return {
            "apikey": apikey,
            "quote_currency": quote_currency,
        }

def _init():
    if not os.path.isfile(HOME + '/.config/forexcast.json'):
        with open(HOME + '/.config/forexcast.json', 'w') as f:
            config = _config()
            if config:
                f.write(json.dumps(config))
            else:
                f.write(json.dumps(default_config))
    with open(HOME + '/.config/forexcast.json', 'r') as f:
        config = json.loads(f.read())
        return config.get("apikey", "-"), config.get("quote_currency", "USD")

def create_df(currency="EUR", from_date="2019-01-01", to_date="2019-12-31", quote_currency="USD", apikey="-"):
    url = "https://cloud.iexapis.com/stable/fx/historical?symbols={}{}&from={}&to={}&token={}".format(quote_currency, currency, from_date, to_date, apikey)
    try:
        response = json.loads(requests.get(url).content)[0]
        data = {"ds": [], "y": []}
        for item in response:
            if item:
                if item.get("rate") and item.get("date"):
                    rate = 1.00 / item.get("rate")
                    date = item.get("date")
                    data["ds"].append(date)
                    data["y"].append(rate)
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        df = None
        return df

def forecast(periods=365, df=None, out=None, currency="EUR", quote_currency="USD"):
    if periods and df is not None:
            m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(df)
            future = m.make_future_dataframe(periods=periods)
            forecast = m.predict(future)
            if out:
                with open(out + "/{}-{}-to-{}.json".format(str(datetime.date.today()), currency, quote_currency), "w") as f:
                    f.write(forecast.to_json())
            fig = plot_plotly(m, forecast)
            fig.update_layout(
                title="{}:{} Forecast".format(currency, quote_currency),
                xaxis_title="Date",
                yaxis_title="Exchange Rate",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                )
            )
            ply.plot(fig)

@click.command()
@click.argument('currency')
@click.option('--from_date', default="2019-01-01", help="Data after this date will be included.")
@click.option('--to_date', default=str(datetime.date.today()), help="Data after this date will be excluded.")
@click.option('--periods', default=365, help='Periods to predict.')
@click.option('--out', default=None, help="If specified will save forecast in specified dir.")
def main(currency, from_date, to_date, periods, out):
    """
    Simple currency forecasting for IEX data

    * CURRENCY = 3 char ISO code for target currency

    * Dates should be in YYYY-MM-DD format
    """
    apikey, quote_currency = _init()
    df = create_df(currency=currency, from_date=from_date, to_date=to_date, quote_currency=quote_currency, apikey=apikey)
    out = os.path.realpath(out) if out else None
    forecast(periods=periods, df=df, out=out, currency=currency, quote_currency=quote_currency)

if __name__ == '__main__':
    main()
