import plotly.express as px

from dash import Dash, Input, Output, State, dcc

from lib.return_provider import ReturnProvider


class StockReturnsChart:
    """Stock returns chart component."""
    def __init__(self, rp: ReturnProvider, app: Dash, start_date, end_date, refresh_button):
        self.comp = dcc.Graph()

        @app.callback(
            Output(self.comp, "figure"),
            State(start_date, "date"),
            State(end_date, "date"),
            Input(refresh_button, "n_clicks")
            )
        def refresh_stock_returns_chart(start_date, end_date, _):
            ret = rp.get_cumulative_return_data(start_date, end_date)
            ret = ret.reset_index()
            ret.columns.name = 'Stock'

            # Using a custom colour sequence to support 10 different colours
            fig = px.line(ret, x='Date', y=ret.columns, color_discrete_sequence=px.colors.qualitative.Alphabet)
            fig.layout.yaxis.tickformat = ',.0%'
            fig.update_layout(xaxis_title=None, yaxis_title=None)

            return fig
