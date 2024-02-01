import dash_bootstrap_components as dbc
from dash import dcc, html


import datetime as dt


SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


class Sidebar:
    """Sidebar component provider."""

    def __init__(self):
        self.start_date = dcc.DatePickerSingle(display_format='D MMM YYYY',
                                               min_date_allowed=dt.date(2000, 1, 1),
                                               max_date_allowed=dt.date(2024, 1, 26),
                                               date=dt.date(2020, 1, 1))
        self.end_date = dcc.DatePickerSingle(display_format='D MMM YYYY',
                                             min_date_allowed=dt.date(2000, 1, 1),
                                             max_date_allowed=dt.date(2024, 1, 26),
                                             date=dt.date(2024, 1, 26))
        self.weighting = dbc.Select(options=[{'label': 'Equal', 'value': 'EQUAL'},
                                             {'label': 'Inverse Vol', 'value': 'INVERSE_VOL'}],
                                    value='EQUAL')
        
        self.refresh = dbc.Button('Refresh')

        self.comp = html.Div([html.H2('Stock Return UI'),
            html.Hr(),
            dbc.Row([dbc.Col(html.H6('Start Date'), style={'text-align': 'right'}),
                     dbc.Col(self.start_date)], align='center', style={'z-index': '9999 !important'}),
            dbc.Row([dbc.Col(html.H6('End Date'), style={'text-align': 'right'}),
                     dbc.Col(self.end_date)], align='center'),
            html.Hr(),
            dbc.Row([dbc.Col(html.H6('Weighting'), style={'text-align': 'right'}),
                     dbc.Col(self.weighting)], align='center'),
            html.Hr(),
            dbc.Row([self.refresh])
            ], style=SIDEBAR_STYLE)
