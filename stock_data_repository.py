"""
Price data are from Yahoo Finance (https://finance.yahoo.com/).
Standing data are from Wiki S&P 500 page (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
"""

import os

import pandas as pd

from typing import Iterator, List
from logging import getLogger
from functools import lru_cache

log = getLogger(__name__)


class StockDataRepository:
    """Stock Data provider."""
    def __init__(self,
                 data_dir: str = 'data',
                 standing_data_file: str = 'standing_data.csv'):
        """Instantiate class

        Args:
            data_dir (str, optional): Directory with the data CSVs. Defaults to 'data'.
            standing_data_file (str, optional): The file with stock standing data. Defaults to 'standing_data.csv'.
        """
        self.__data_dir = data_dir
        self.__standing_data_file = standing_data_file

    def get_stocks_with_prices(self) -> Iterator[str]:
        """Get the tickers for stocks that have prices in the data dir.

        Yields:
            Iterator[str]: The tickers of the stocks found one by one.
        """
        for f in os.listdir(self.__data_dir):
            if not f.endswith('.csv') or f.lower() == self.__standing_data_file.lower():
                continue

            yield f[:-4]

    @lru_cache(maxsize=10)
    def get_stock_price_data(self, ticker: str) -> pd.DataFrame:
        """Return price data for stock. Stock must have a CSV in the data dir.

        Args:
            ticker (str): The ticker to get prices for.

        Returns:
            pd.DataFrame: A dataframe with the CSV data
        """
        d = os.path.join(self.__data_dir, f'{ticker}.csv')
        log.info('Loading price for %s from %s', ticker, d)

        return pd.read_csv(d, parse_dates=['Date'])

    @property
    @lru_cache(maxsize=1)
    def __standing_data(self) -> pd.DataFrame:
        """Private property to hold the full standing data table.

        Returns:
            pd.DataFrame: All standing data available.
        """
        d = os.path.join(self.__data_dir, self.__standing_data_file)
        log.info('Loading standing data from %s', d)

        ret = pd.read_csv(d)
        del ret['Date added']  # Date added to S&P500, irrelevant column
        return ret

    def get_stock_standing_data(self, tickers: List[str]) -> pd.Series:
        """Get standing data for a stock.

        Args:
            tickers (List[str]): The tickers to get standing data for.

        Returns:
            pd.Series: All available standing data for the tickers requested.
        """
        ss = self.__standing_data
        return ss.loc[ss['Symbol'].isin(tickers)]


if __name__ == "__main__":

    import logging
    logging.basicConfig(format='%(asctime)s: %(name)s|%(levelname)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger(__name__).setLevel(logging.INFO)

    sdr = StockDataRepository()
    msft = sdr.get_stock_price_data('MSFT')
    print(list(sdr.get_stocks_with_prices()))
    print(msft)

    sd = sdr.get_stock_standing_data('MSFT')
    print(sd)
