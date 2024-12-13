# layouts.py
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from Tabs import *

def create_layout(app: Dash):
    return html.Div([
        html.Div(
            className="banner",
            style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "100px", "position": "relative", "margin": "0 auto", "background-color": "#28334AFF", "color": "white"}, 
            children=[
                html.Div(
                    className="logo-container",
                    style={"flex-grow": "0"},
                    children=[
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="logo",
                            style={"width": "180px", "height": "90px"},
                        ),
                    ],
                ),
                html.Div(
                    className="title-container",
                    style={"flex-grow": "1"},
                    children=[
                        html.H1(
                            "Stats Explorer Summary of the NBA",
                            className="title",
                            style={"margin-bottom": "0", "font-size": "42px", "text-align": "center"},  # Aumentar el tamaño de fuente
                        ),
                    ],
                ),
                html.Div(
                    className="author-info",
                    children=[
                        html.H3(
                            "By: Jesus Ochoa",
                            className="author-name",
                            style={"margin-bottom": "0", "font-size": "16px", "margin-right": "10px", "display": "inline"}
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url("linkedin_logo.jpg"),
                                className="linkedin-logo",
                                style={"width": "30px", "height": "auto", "background-color": "#28334AFF", "color": "#28334AFF"},
                            ),
                            href="https://www.linkedin.com/in/jesus-alberto-ochoa/",
                            target="_blank",
                        )
                    ],
                    style={"position": "absolute", "bottom": "0", "right": "0", "margin": "20px"}
                )
            ],
        ),
    dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='General Information by Seasons', value='tab-1', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}),
            dcc.Tab(label='Stats per Player Season',        value='tab-2', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}),
            dcc.Tab(label='Statistical Models',             value='tab-3', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}),
                    ]),
    html.Div(id='tab-content')
])

