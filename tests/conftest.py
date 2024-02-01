import pytest

import pandas as pd

from unittest.mock import Mock
from typing import List

from lib.return_provider import ReturnProvider
from lib.portfolio_performance import PortfolioPerformanceProvider


@pytest.fixture
def tickers() -> List[str]:
    """Fixed list of tickers to align tests."""
    return ['MSFT', 'AAPL', 'GOOG']

@pytest.fixture
def mock_sdr(tickers):
    """Providing a mock Stock Data Repository to avoid hitting the disk."""
    sdr = Mock()
    sdr.get_stocks_with_prices.return_value = tickers

    # many dates, and all prices = 1
    idx = pd.date_range(pd.Timestamp(1980, 1, 1), pd.Timestamp(2030, 1, 1))
    sdr.get_stock_price_data.return_value = pd.DataFrame(data={'Date': idx,
                                                               'Adj Close': [1] * len(idx)})
    sdr.get_stock_standing_data.return_value = pd.DataFrame({'Symbol': tickers,
                                                             'GICS Sector': ['IT', 'IT', 'IT2']})

    return sdr

@pytest.fixture
def rp(mock_sdr) -> ReturnProvider:
    """Providing a Return Provider implementation that uses the mocl."""
    return ReturnProvider(sdr=mock_sdr)

@pytest.fixture
def ppp(mock_sdr, rp) -> PortfolioPerformanceProvider:
    return PortfolioPerformanceProvider(rp=rp, sdr=mock_sdr)
