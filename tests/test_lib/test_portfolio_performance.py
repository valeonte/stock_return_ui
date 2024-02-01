import pandas as pd

from typing import List

from lib.portfolio_performance import PortfolioPerformanceProvider, Weighting


def test_calculate_portfolio_performance_weighting(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert perf.weighting == weighting

def test_calculate_portfolio_performance_tickers(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert all([t in tickers for t in perf.tickers])

def test_calculate_portfolio_performance_cum_perf(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert (perf.port_cum_perf == 0).all()

def test_calculate_portfolio_performance_stock_contributions(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert (perf.stock_contributions == 0).all().all()

def test_calculate_portfolio_performance_stock_contributions_columns(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert perf.stock_contributions.columns.isin(tickers).all()

def test_calculate_portfolio_performance_sector_contrib_columns(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert len(perf.sector_contribution.columns) == 2

def test_calculate_portfolio_performance_sector_contributions(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert (perf.sector_contribution == 0).all().all()

def test_calculate_portfolio_performance_stock_weights(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert (perf.stock_weights == 1/len(tickers)).all().all()

def test_calculate_portfolio_performance_stock_weights(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert perf.stock_weights.columns.isin(tickers).all()

def test_calculate_portfolio_performance_sector_weights_columns(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert len(perf.sector_weights.columns) == 2

def test_calculate_portfolio_performance_sector_weights(ppp: PortfolioPerformanceProvider, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    weighting = Weighting.EQUAL
    perf = ppp.calculate_portfolio_performance(from_date, to_date, tickers, weighting)

    assert (perf.sector_weights.sum(1) == 1).all()


if __name__ == "__main__":
    import pytest

    pytest.main()
