
import pandas as pd

from typing import List

from lib.stock_data_repository import StockDataRepository


class ReturnProvider:
    """Class to provide stock return data for charting."""
    def __init__(self, sdr: StockDataRepository = None):
        """Instantiate class with optional injected dependency."""
        self.__sdr = sdr or StockDataRepository()

    def get_stock_return_data(self,
                              from_date: pd.Timestamp,
                              to_date: pd.Timestamp,
                              tickers: List[str] = None) -> pd.DataFrame:
        """Calculate daily return for optionally all, tickers.

        Args:
            from_date (pd.Timestamp): Start date of the requested period
            to_date (pd.Timestamp): End date of the requested period
            tickers (List[str], optional): List of tickers to pull, defaults to all available. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with date as index and one column per ticker with daily return.
        """
        if tickers is None:
            tickers = list(self.__sdr.get_stocks_with_prices())
        
        all_data = []
        for t in tickers:
            p = self.__sdr.get_stock_price_data(t)
            ret = p.loc[p['Date'].between(from_date, to_date), ['Date', 'Adj Close']
                        ].set_index('Date')[['Adj Close']].pct_change().fillna(0)
            ret.columns = [t]
            all_data.append(ret)
        
        return pd.concat(all_data, axis=1)
    
    def get_cumulative_return_data(self,
                                   from_date: pd.Timestamp,
                                   to_date: pd.Timestamp,
                                   tickers: List[str] = None) -> pd.DataFrame:
        """Calculate cumulative daily return for optionally all, tickers.

        Args:
            from_date (pd.Timestamp): Start date of the requested period
            to_date (pd.Timestamp): End date of the requested period
            tickers (List[str], optional): List of tickers to pull, defaults to all available. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with date as index and one column per ticker with daily cumulative return.
        """
        ret = self.get_stock_return_data(from_date=from_date, to_date=to_date, tickers=tickers)
        return (ret + 1).cumprod() - 1


if __name__ == "__main__":
    
    rp = ReturnProvider()

    ret = rp.get_cumulative_return_data(pd.Timestamp(2010, 1, 1), pd.Timestamp(2024, 1, 1))

    print(ret)
