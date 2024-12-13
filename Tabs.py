# tabs.py
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from Controller import Group_By_Mean
import pandas as pd

# Import Data
df       = pd.read_excel("BBDD.xlsx")
dfplayer = pd.read_excel("BBDD_Player.xlsx")
# Transform Df 
dfMean = Group_By_Mean(df)

def tab_general_information():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-season',
                options=[
                    {'label': Season, 'value': Season} for Season in dfMean['SEASON'].unique()
                ],
                value=dfMean['SEASON'].iloc[0],
                style={
                    'background-color': 'White', 
                    'color': 'black',  
                    'font-weight': 'bold',
                    'margin-top': '30px'  
                }
            ), 
        ], style={'text-align': 'center', 'margin-bottom': '20px'}),

        html.Div(children=[
            html.Div(children=[
                html.H2('Average Points', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Average', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '24%', 'margin-top': '20px'}),

        html.Div(children=[
            html.Div(children=[
                html.H2('Free Throws', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Free_Throws', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '24%', 'margin-top': '20px'}),

        html.Div(children=[
            html.Div(children=[
                html.H2('Two Points', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Two_Points', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '24%', 'margin-top': '20px'}),

        html.Div(children=[
            html.Div(children=[
                html.H2('Three Points', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Three_Points', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '24%', 'margin-top': '20px'}),

        dcc.Tabs(id='inner-tabs', value='graph-1', children=[
            dcc.Tab(label='Baskets by Area and Seasons',                                    value='graph-1', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}),  
            dcc.Tab(label='Historical Evolution of Shooting Percentages According to Area', value='graph-2', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}) 
        ], style={'margin-top': '30px', 'background-color': 'White',  'color': 'black',  'font-weight'     : 'bold'}),

        html.Div(id='inner-tab-content'),

        html.Div([
            html.H2('Statistics by Team and Season', style={'text-align': 'center', "background-color": "#28334AFF", "color": "white","font-size": "35px"}),
            dcc.Dropdown(
                id='column-selector',
                options=[{'label': col, 'value': col} for col in df.columns if col not in ['Unnamed: 0','SEASON', 'TEAM', 'W', 'L']],
                value=[],  # Columnas por defecto
                multi=True,
                style={'width': '95%', 'margin': 'auto', 'margin-bottom': '20px'}
            ),
            dash_table.DataTable(
                id='team-stats-table',
                columns=[{'name': col, 'id': col} for col in ['Team', 'W', 'L'] if col not in ['Unnamed: 0','SEASON']],  # Columna para el nombre del equipo
                data=[],

                style_table={
                    'overflowX': 'auto',  # Habilita el desplazamiento horizontal si es necesario
                    'border': '1px solid #d6d6d6',
                    'maxHeight': '400px',
                    'maxWidth': 'none',
                    'backgroundColor': '#28334AFF', 
                },
                style_header={
                    'backgroundColor': '#28334AFF',  # Color de fondo del encabezado
                    'fontWeight': 'bold',  # Encabezado en negrita
                    'color': 'white',  # Color del texto del encabezado
                    'text-align': 'center',  # Alineación centrada del texto del encabezado
                    'fontSize': '18px',  # Tamaño de fuente del encabezado
                },
                style_cell={
                    'font-family': 'Segoe UI',  # Define la fuente del texto en las celdas
                    'font-size': '16px',  # Define el tamaño de fuente en las celdas
                    'text-align': 'center',  # Centra el texto en las celdas
                    'minWidth': '120px',  # Establece el ancho mínimo de las celdas
                    'whiteSpace': 'normal',  # Controla el desbordamiento del texto
                    'height': 'auto',  # Altura automática para el contenido de las celdas
                    'backgroundColor': '#f9f9f9',  # Color de fondo de las celdas
                    'color': '#333',  # Color de texto en las celdas
                    'border': '1px solid #d6d6d6',  # Añade un borde a las celdas
                    'fontWeight': 'bold',  # Texto en negrita
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f2f2f2'  # Alterna el color de fondo de las filas impares
                    },
                ],
                sort_action='native',  # Habilita la ordenación
                sort_mode='multi',  # Permite ordenación en múltiples columnas
                fixed_rows={'headers': True},
                fixed_columns={'headers': True, 'data': 1},  # Fija la primera columna (encabezados) y una columna de datos

            )
        ])
    ])

def tab_stats_per_player():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-season-player',
                options=[
                    {'label': Season, 'value': Season} for Season in dfplayer['Season'].unique()
                ],
                value=dfplayer['Season'].iloc[0],
                style={
                    'background-color': 'White', 
                    'color': 'black',  
                    'font-weight': 'bold',
                    'margin-top': '30px'  
                }
            ), 
        ], style={'text-align': 'center', 'margin-bottom': '20px'}),

            # Botones de filtrado
    html.Div([
        html.Button('All Position', id='button-all', n_clicks=0, className='filter-button'),
        html.Button('Guard',        id='button-guard', n_clicks=0, className='filter-button'),
        html.Button('Fordward',     id='button-fordward', n_clicks=0, className='filter-button'),
        html.Button('Center',       id='button-center', n_clicks=0, className='filter-button'),
    ], style={
        'display': 'flex', 
        'justify-content': 'center', 
        'gap': '10px', 
        'margin-top': '20px'
    }),

    html.Div(children=[
            html.Div(children=[
                html.H2('Average Age', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Age', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),
    
    html.Div(children=[
            html.Div(children=[
                html.H2('Average Pts', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Points_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),
    
    html.Div(children=[
            html.Div(children=[
                html.H2('Average Reb', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Reb_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),
    
    html.Div(children=[
            html.Div(children=[
                html.H2('Average Ast', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Ast_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),

    html.Div(children=[
            html.Div(children=[
                html.H2('Average Blk', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Blk_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),

    html.Div(children=[
            html.Div(children=[
                html.H2('Average Stl', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Stl_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),

    html.Div(children=[
            html.Div(children=[
                html.H2('Average Tov', style={'margin-bottom': '10px', 'text-align': 'center','color': 'white', 'font-weight': 'bold'}),
                html.H3(id='Tov_Player', style={'font-size': '30px', 'text-align': 'center', 'margin-top': '-10px','color': 'white', 'font-weight': 'bold'})
            ], style={'padding': '18px', 'border-radius': '5px', 'background': 'linear-gradient(to bottom, #191970, #00BFFF)', 'height': '65px'}),
        ], style={'display': 'inline-block', 'margin-left': '8px', 'width': '13.7%', 'margin-top': '20px'}),

        dcc.Tabs(id='inner-tabs-players', value='graph-3', children=[
            dcc.Tab(label='Baskets by Area and Seasons',                                    value='graph-3', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}),  
            dcc.Tab(label='PIE by Position-Age Group', value='graph-4', style={'font-weight': 'bold', 'background': 'linear-gradient(to bottom, #28334AFF, #00BFFF)', 'color': 'white'}) 
        ], style={'margin-top': '30px', 'background-color': 'White',  'color': 'black',  'font-weight'     : 'bold'}),

        html.Div(id='inner-tab-content-player'),
    html.Div([
            html.H1("Compare Players' Seasons", style={'text-align': 'center', "background-color": "#28334AFF", "color": "white","font-size": "35px"}),  # Título
            # Primer par de dropdowns
                html.Div([
                    dcc.Dropdown(
                        id="season-dropdown-1",
                        options=[{"label": season, "value": season} for season in dfplayer["Season"].unique()],
                        placeholder="Select a Season",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "margin-right": "10px", 
                                "display": "inline-block", 
                                "width": "165px", 
                                "text-align": "center"
                            }
                    ),
                    dcc.Dropdown(
                        id="player-dropdown-1",
                        options=[{"label": player, "value": player} for player in dfplayer["Player"].unique()],
                        placeholder="Select a Player",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "250px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    ),
                    dcc.Dropdown(
                        id="stats-dropdown-p1",
                        options=[{"label": col, "value": col} for col in dfplayer.columns if col not in ["Season", "Player"]],
                        multi=True,
                        placeholder="Select Stats",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "350px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    )
                ], style={
                                "margin-bottom": "20px",
                                "display": "flex",
                                "justify-content": "center",  # Centrar horizontalmente
                                "align-items": "center"       # Alinear verticalmente
                            }),
                # Segundo jugador
                html.Div([
                    dcc.Dropdown(
                        id="season-dropdown-2",
                        options=[{"label": season, "value": season} for season in dfplayer["Season"].unique()],
                        placeholder="Select a Season",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "margin-right": "10px", 
                                "display": "inline-block", 
                                "width": "165px", 
                                "text-align": "center"
                            }
                    ),
                    dcc.Dropdown(
                        id="player-dropdown-2",
                        options=[{"label": player, "value": player} for player in dfplayer["Player"].unique()],
                        placeholder="Select a Player",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "250px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    ),
                    dcc.Dropdown(
                        id="stats-dropdown-p2",
                        options=[{"label": col, "value": col} for col in dfplayer.columns if col not in ["Season", "Player"]],
                        multi=True,
                        placeholder="Select Stats",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "350px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    )
                ], style={
                                "margin-bottom": "20px",
                                "display": "flex",
                                "justify-content": "center",  # Centrar horizontalmente
                                "align-items": "center"       # Alinear verticalmente
                            }),
                # Tercer jugador
                html.Div([
                    dcc.Dropdown(
                        id="season-dropdown-3",
                        options=[{"label": season, "value": season} for season in dfplayer["Season"].unique()],
                        placeholder="Select a Season",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "margin-right": "10px", 
                                "display": "inline-block", 
                                "width": "165px", 
                                "text-align": "center"
                            }
                    ),
                    dcc.Dropdown(
                        id="player-dropdown-3",
                        options=[{"label": player, "value": player} for player in dfplayer["Player"].unique()],
                        placeholder="Select a Player",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "250px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    ),

                    dcc.Dropdown(
                        id="stats-dropdown-p3",
                        options=[{"label": col, "value": col} for col in dfplayer.columns if col not in ["Season", "Player"]],
                        multi=True,
                        placeholder="Select Stats",
                        style={
                                "font-weight": "bold",
                                "color": "black", 
                                "width": "350px", 
                                "display": "inline-block", 
                                "margin-left": "10px",
                                "text-align": "center"
                            }
                    )
                ], style={
                                "margin-bottom": "20px",
                                "display": "flex",
                                "justify-content": "center",  # Centrar horizontalmente
                                "align-items": "center"       # Alinear verticalmente
                            }),
            ], style={
                        "background-color": "#FFFFFF",
                        "padding": "15px",
                        "border-radius": "8px",
                        "box-shadow": "0px 2px 5px rgba(0, 0, 0, 0.1)",
                        "margin": "20px auto",
                        "width": "90%"
}),
   html.Div(id="tables-container", style={"display": "flex", "justify-content": "space-evenly"}),
])


def tab_statistical_models():
    return html.Div([
        # Aquí puedes agregar los componentes para mostrar las estadísticas de jugadores
    ])

def tab_download_data():
    return html.Div([
        # Aquí puedes agregar los componentes para realizar los modelos estadísticos
    ])
