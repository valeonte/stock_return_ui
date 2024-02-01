import dash_bootstrap_components as dbc

from dash import Dash
from dash_bootstrap_templates import load_figure_template
from components.main_content import MainContent
from components.sidebar import Sidebar


class AppCreator:
    """App instantiator."""

    def create_app(self):
        """Create the Dash app, and return the Flask server to host

        Returns:
            Flask: The Flask aplication server
        """
        app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        load_figure_template('BOOTSTRAP')

        sidebar = Sidebar()
        main = MainContent(app, sidebar)

        app.layout = dbc.Container(dbc.Row([dbc.Col(sidebar.comp, width=3),
                                            dbc.Col(main.comp)]))

        return app.server

