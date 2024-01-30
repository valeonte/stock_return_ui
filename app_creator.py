import plotly.express as px
import pandas as pd

from dash import Dash, html, dash_table, dcc

from stock_data_repository import StockDataRepository
from return_provider import ReturnProvider


class AppCreator:
    """App instantiator."""

    def create_app(self):
        """Create the Dash app, and return the Flask server to host

        Returns:
            Flask: The Flask aplication server
        """
        app = Dash(__name__)

        sdr = StockDataRepository()
        rp = ReturnProvider(sdr)
        ret = rp.get_cumulative_return_data(pd.Timestamp(2010, 1, 1), pd.Timestamp(2024, 1, 1))
        ret = ret.reset_index()
        ret.columns.name = 'Stocks'
        sd = sdr.get_stock_standing_data(ret.columns)

        fig = px.line(ret, x='Date', y=ret.columns)
        fig.update_layout(yaxis_title='Return')
        app.layout = html.Div([
            html.Div(children='Stock returns plot'),
            html.Hr(),
            dcc.Graph(figure=fig, id='controls-and-graph'),
            dash_table.DataTable(data=sd.to_dict('records'), page_size=10),
        ])

        return app.server

