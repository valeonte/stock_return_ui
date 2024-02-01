import dash_bootstrap_components as dbc

from lib.stock_data_repository import StockDataRepository
from typing import List


class StockDataTable:
    """Provider for the stock data table component.
    
    Just populate the stock standing data table.
    """

    def __init__(self, sdr: StockDataRepository, tickers: List[str]):
        """Instantiates the component.

        Args:
            sdr (StockDataRepository): Will need the repository to pull stock details
            tickers (List[str]): A list of tickers to return data for.
        """
        # Nothing dynamic for this table, so nothing exposed other than the comp
        sd = sdr.get_stock_standing_data(tickers)
        self.comp = dbc.Table.from_dataframe(sd, striped=True, bordered=True, hover=True)
