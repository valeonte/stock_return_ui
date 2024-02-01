import plotly.express as px

from dash import Dash, Input, Output, State, dcc
from typing import List

from lib.portfolio_performance import PortfolioPerformanceProvider, Weighting


class PortfolioPerformanceComponents:
    """Stock returns chart component."""
    def __init__(self, ppp: PortfolioPerformanceProvider, app: Dash,
                 tickers: List[str],
                 start_date, end_date, weighting, refresh_button):
        self.port_cum_perf = dcc.Graph()
        self.port_stock_weights = dcc.Graph()
        self.port_stock_contr = dcc.Graph()
        self.port_sector_contr = dcc.Graph()
        self.port_sector_weights = dcc.Graph()

        @app.callback(
            Output(self.port_cum_perf, "figure"),
            Output(self.port_stock_weights, "figure"),
            Output(self.port_stock_contr, "figure"),
            Output(self.port_sector_contr, "figure"),
            Output(self.port_sector_weights, "figure"),
            State(start_date, "date"),
            State(end_date, "date"),
            State(weighting, "value"),
            Input(refresh_button, "n_clicks")
            )
        def refresh_portfolio_return_comps(start_date, end_date, weighting, _):
            """Callback to refresh all portfolio performance related components."""

            # Extract performance data
            perf = ppp.calculate_portfolio_performance(start_date, end_date, tickers, Weighting[weighting])
            ret = perf.port_cum_perf.reset_index()
            ret.columns = ['Date', 'Portfolio']

            # Plot portfolio performance
            port_perf = px.line(ret, x='Date', y='Portfolio')
            port_perf.layout.yaxis.tickformat = ',.0%'
            port_perf.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)

            # Plot weights
            wgts = perf.stock_weights.reset_index().melt(var_name='Stock', value_name='Weight', id_vars=('Date', ))
            
            swgt = px.area(wgts, x='Date', y='Weight', color='Stock', color_discrete_sequence=px.colors.qualitative.Alphabet)
            swgt.layout.yaxis.tickformat = ',.0%'
            swgt.update_layout(xaxis_title=None, yaxis_title=None)

            # Stock contributions
            ret = (perf.stock_contributions + 1).cumprod() - 1
            ret = ret.reset_index()
            ret.columns.name = 'Stock'

            scontr = px.line(ret, x='Date', y=ret.columns, color_discrete_sequence=px.colors.qualitative.Alphabet)
            scontr.layout.yaxis.tickformat = ',.0%'
            scontr.update_layout(xaxis_title=None, yaxis_title=None)

            # Sector contributions
            ret = (perf.sector_contribution + 1).cumprod() - 1
            ret = ret.reset_index()
            ret.columns.name = 'Sector'

            secontr = px.line(ret, x='Date', y=ret.columns, color_discrete_sequence=px.colors.qualitative.Alphabet)
            secontr.layout.yaxis.tickformat = ',.0%'
            secontr.update_layout(xaxis_title=None, yaxis_title=None)

            # Plot sector weights
            wgts = perf.sector_weights.reset_index().melt(var_name='Sector', value_name='Weight', id_vars=('Date', ))
            
            secwgt = px.area(wgts, x='Date', y='Weight', color='Sector', color_discrete_sequence=px.colors.qualitative.Alphabet)
            secwgt.layout.yaxis.tickformat = ',.0%'
            secwgt.update_layout(xaxis_title=None, yaxis_title=None)

            return port_perf, swgt, scontr, secontr, secwgt
