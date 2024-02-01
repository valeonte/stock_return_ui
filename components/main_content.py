import dash_bootstrap_components as dbc

from dash import dcc

from dash import Dash
from components.stock_data_table import StockDataTable

from components.sidebar import Sidebar
from components.stock_returns_chart import StockReturnsChart
from components.port_performance_components import PortfolioPerformanceComponents

from lib.return_provider import ReturnProvider
from lib.stock_data_repository import StockDataRepository
from lib.portfolio_performance import PortfolioPerformanceProvider


class MainContent:
    """Main content component provider."""
    def __init__(self, app: Dash, sidebar: Sidebar):
        self.sidebar = sidebar
        self.app = app

        sdr = StockDataRepository()
        rp = ReturnProvider(sdr=sdr)
        ppp = PortfolioPerformanceProvider(rp=rp, sdr=sdr)

        tickers = list(sdr.get_stocks_with_prices())

        src = StockReturnsChart(rp, app, sidebar.start_date, sidebar.end_date, sidebar.refresh)
        sdt = StockDataTable(sdr, tickers)
        ppc = PortfolioPerformanceComponents(ppp, app, tickers, sidebar.start_date, sidebar.end_date, sidebar.weighting, sidebar.refresh)

        self.comp = dcc.Tabs([
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading(src.comp))), label='Stock Returns'),
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading([ppc.port_cum_perf, ppc.performance_table]))), label='Portfolio Performance'),
            dcc.Tab(dbc.Card(dbc.CardBody(sdt.comp)), label='Stock Details'),
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading(ppc.port_stock_weights))), label='Stock Weights'),
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading(ppc.port_stock_contr))), label='Stock Contributions'),
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading(ppc.port_sector_weights))), label='Sector Weights'),
            dcc.Tab(dbc.Card(dbc.CardBody(dcc.Loading(ppc.port_sector_contr))), label='Sector Contributions')
            ])
