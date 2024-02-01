
import pandas as pd
import numpy as np

from typing import List
from enum import Enum
from logging import getLogger
from dataclasses import dataclass

from lib.return_provider import ReturnProvider
from lib.stock_data_repository import StockDataRepository


log = getLogger(__name__)


class Weighting(Enum):
    EQUAL = 1
    INVERSE_VOL = 2


@dataclass
class PortfolioPerformanceData:
    """Data struct to hold portfolio performance results."""

    tickers: List[str]
    weighting: Weighting
    port_cum_perf: pd.Series
    stock_contributions: pd.DataFrame
    stock_weights: pd.DataFrame
    sector_contribution: pd.DataFrame
    sector_weights: pd.DataFrame

    port_ann_ret: float
    port_ann_vol: float

    @property
    def port_sharpe_ratio(self):
        return self.port_ann_ret / self.port_ann_vol


class PortfolioPerformanceProvider:
    """Constructs hypothetical portfolios and calculates performance.
    
    To avoid repeating calculations, we produce all the portfolio performance relevant data in one go,
    as they all use the same underlying data.
    """
    def __init__(self, rp: ReturnProvider = None, sdr: StockDataRepository = None, inverse_vol_window_weeks: int = 156):
        # Injecting the dependencies here, but also instantiating if not provided for easier debugging
        self.__sdr = sdr or StockDataRepository()
        self.__rp = rp or ReturnProvider(self.__sdr)
        self.inverse_vol_window_weeks = inverse_vol_window_weeks

    def calculate_portfolio_performance(self,
                                        from_date: pd.Timestamp,
                                        to_date: pd.Timestamp,
                                        tickers: List[str],
                                        weighting: Weighting) -> PortfolioPerformanceData:
        """Calculate cumulative portfolio performance between dates.

        Args:
            from_date (pd.Timestamp): Start date of period
            to_date (pd.Timestamp): End date of period
            tickers (List[str]): List of tickers to include in portfolio
            weighting (Weighting): Weighting to use when constructing portfolio

        Returns:
            PortfolioPerformanceData: The portfolio performance data, in an appropriate struct
        """
        log.info('Calculating portfolio performance for %d assets from %s to %s with weighting %s',
                 len(tickers), from_date, to_date, weighting)
        # Extract stock return data
        ret = self.__rp.get_stock_return_data(from_date, to_date, tickers)

        # Determin the weights on any day
        wgt = pd.DataFrame(index=ret.index, columns=ret.columns)
        if weighting == Weighting.EQUAL:
            # On equal, calculate the asset weight on each day using assets with return only
            day_weight = 1/(~ret.isna()).sum(1)
            # The apply the weights in the same fashion, populating only non-NA cells
            for col in ret.columns:
                mask = ~ret[col].isna()
                wgt.loc[mask, col] = day_weight[mask]
        elif weighting == Weighting.INVERSE_VOL:
            # Extending history to calculate vols
            new_to_date = ret.index.min() - pd.offsets.BDay(1)
            new_from_date = new_to_date - pd.offsets.Week(self.inverse_vol_window_weeks)
            pre_ret = self.__rp.get_stock_return_data(new_from_date, new_to_date, tickers)
            ext_ret = pd.concat([pre_ret, ret])
            
            # Calculating rolling vol
            # Resampling to weekly to calculate vol
            ext_ret = (ext_ret + 1).resample('W-FRI').prod() - 1
            vol = ext_ret.rolling(window=self.inverse_vol_window_weeks, min_periods=self.inverse_vol_window_weeks//2).std()
            # Back to daily, aligning with returns and inversing
            vol = 1 / vol.resample('B').ffill().reindex(ret.index)
            # The apply the weights in the same fashion, populating only non-NA cells
            for col in ret.columns:
                mask = ~ret[col].isna() & ~vol[col].isna()
                wgt.loc[mask, col] = vol.loc[mask, col]

            wgt = wgt.div(wgt.sum(1), axis=0)

        # Calculate daily stock contributions
        contr = ret.multiply(wgt)

        # Building sector contributions and weights
        stock_data = self.__sdr.get_stock_standing_data(tickers)
        sectors = stock_data['GICS Sector'].drop_duplicates()
        sector_contr = pd.DataFrame(index=contr.index, columns=sectors)
        sector_wgt = pd.DataFrame(index=contr.index, columns=sectors)
        for sec in sectors:
            sec_stocks = stock_data.loc[stock_data['GICS Sector'] == sec, 'Symbol']
            sector_contr.loc[:, sec] = contr.loc[:, contr.columns.isin(sec_stocks)].sum(1)
            sector_wgt.loc[:, sec] = wgt.loc[:, wgt.columns.isin(sec_stocks)].sum(1)

        # Sum to get portfolio daily return
        port_ret = contr.sum(1)
        
        # Annualised volatility
        ann_vol = port_ret.std() * np.sqrt(252)

        # Cumulative product to get cumulative return
        cum_ret = (port_ret + 1).cumprod() - 1
        
        # Annualised return
        ann_ret = (cum_ret.iloc[-1] + 1) ** (252/len(cum_ret)) - 1

        # Construct the struct to return
        pp = PortfolioPerformanceData(tickers=tickers, weighting=weighting,
                                      port_cum_perf=cum_ret, stock_contributions=contr,
                                      stock_weights=wgt, sector_contribution=sector_contr,
                                      sector_weights=sector_wgt,
                                      port_ann_ret=ann_ret, port_ann_vol=ann_vol)

        return pp


if __name__ == "__main__":
    import logging
    logging.basicConfig(format='%(asctime)s: %(name)s|%(levelname)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger(__name__).setLevel(logging.INFO)

    ppp = PortfolioPerformanceProvider()
    perf = ppp.calculate_portfolio_performance(pd.Timestamp(2010, 1, 1), pd.Timestamp(2024, 1, 1),
                                               ['MSFT', 'AAPL', 'BA', 'MMM'],
                                               Weighting.INVERSE_VOL)
    print(perf)
