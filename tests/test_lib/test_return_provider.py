import pandas as pd

from typing import List

from lib.return_provider import ReturnProvider


def test_get_stock_return_data_columns_are_tickers(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_stock_return_data(from_date, to_date, tickers)

    assert ret.columns.isin(tickers).all()

def test_get_stock_return_data_return_flat(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_stock_return_data(from_date, to_date, tickers)

    assert (ret == 0).all().all()

def test_get_stock_return_data_dates(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_stock_return_data(from_date, to_date, tickers)

    assert ret.index.min() >= from_date
    assert ret.index.max() <= to_date


def test_get_cumulative_return_data_columns_are_tickers(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_cumulative_return_data(from_date, to_date, tickers)

    assert ret.columns.isin(tickers).all()

def test_get_cumulative_return_data_return_flat(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_cumulative_return_data(from_date, to_date, tickers)

    assert (ret == 0).all().all()

def test_get_cumulative_return_data_dates(rp, tickers: List[str]):
    from_date = pd.Timestamp(2010, 1, 1)
    to_date = pd.Timestamp(2020, 1, 1)
    ret = rp.get_cumulative_return_data(from_date, to_date, tickers)

    assert ret.index.min() >= from_date
    assert ret.index.max() <= to_date


if __name__ == "__main__":
    import pytest

    pytest.main()
