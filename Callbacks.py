# callbacks.py
from dash import Dash
from dash.dependencies import Input, Output, State, MATCH
import dash_core_components as dcc
from dash import callback_context, dash_table, html 
from Tabs import tab_general_information, tab_stats_per_player, tab_statistical_models, tab_download_data
import pandas as pd
import plotly.express as px
from Controller import *

# Import Data
df            = pd.read_excel("BBDD.xlsx")
dfplayer      = pd.read_excel("BBDD_Player.xlsx")
dfplayer      = dfplayer[(dfplayer["GP"] >=20) & (dfplayer["MIN"]/dfplayer["GP"] >=20)] #Criterio de inclusion de jugador
dfMean        = Group_By_Mean(df)
custom_colors = ['#191970', '#0000FF', '#6495ED', '#87CEFA', '#9EB2E0']

def register_callbacks(app: Dash):
    @app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            return tab_general_information()
        elif tab == 'tab-2':
            return tab_stats_per_player()
        elif tab == 'tab-3':
            return tab_statistical_models()
        elif tab == 'tab-4':
            return tab_download_data()

    @app.callback(
        Output('Average', 'children'),
        [Input('dropdown-season', 'value')]
    )
    def update_average(season_selected):
        df_filtrado   = dfMean[(dfMean['SEASON'] == season_selected)]
        Average_Point = df_filtrado["PTS"].values[0]
        return Average_Point

    @app.callback(
        [Output('Free_Throws', 'children'),
         Output('Two_Points', 'children'),
         Output('Three_Points', 'children')],
        [Input('dropdown-season', 'value')]
    )
    def update_counters(season_selected):
        df_filtrado = dfMean[(dfMean['SEASON'] == season_selected)]
        Free_Throws = f"{df_filtrado['PTS_FT%'].values[0]}%"
        Two_Points = f"{df_filtrado['PTS_2PT%'].values[0]}%"
        Three_Points = f"{df_filtrado['PTS_3PT%'].values[0]}%"
        return Free_Throws, Two_Points, Three_Points

    @app.callback(
        Output('inner-tab-content', 'children'),
        [Input('inner-tabs', 'value')]
    )
    def render_inner_content(tab):
        if tab == 'graph-1':
            return dcc.Graph(id='Stats-chart', style={'margin-top': '20px'})
        elif tab == 'graph-2':
            return dcc.Graph(id='line-chart',  style={'margin-top': '20px'})

    @app.callback(
        Output('line-chart', 'figure'),
        Input('dropdown-season', 'value')
    )
    def update_line_chart(season_selected):
        fig_Historical_Line = px.line(dfMean, x='Season', y=['PTS_2PT_MR%', 'PTS_PITP%', 'PTS_3PT%', 'PTS_FT%'],
                              color_discrete_sequence=custom_colors, markers=True)

        fig_Historical_Line.update_traces(line=dict(width=2.5))

        fig_Historical_Line.update_layout(plot_bgcolor='white', 
                    yaxis_title='',
                    xaxis_title= '',
                    legend_title_text='Shooting Area')
        return fig_Historical_Line

    @app.callback(
        Output('Stats-chart', 'figure'),
        Input('dropdown-season', 'value')
    )
    def update_bar_chart(season_selected):
        df_filtered = df[df['SEASON'] == season_selected]
        df_filtered = df_filtered.sort_values(by='PTS_2PT_MR%', ascending=True)

        fig = px.bar(df_filtered, x='TEAM', y=['PTS_2PT_MR%', 'PTS_PITP%', 'PTS_3PT%', 'PTS_FT%'],
                     height=400,
                     barmode='stack',
                     color_discrete_sequence=custom_colors
                     )

        fig.update_layout(plot_bgcolor='white', 
                          yaxis_title='', 
                          xaxis_title='',
                          legend_title_text='Shooting Area')
        return fig

    @app.callback(
        [Output('team-stats-table', 'columns'),
         Output('team-stats-table', 'data')],
        [Input('dropdown-season', 'value'),
         Input('column-selector', 'value')]
    )
    def update_table(season_selected, selected_columns):
        df_filtered = df[df['SEASON'] == season_selected]
        columns = [{'name': col, 'id': col} for col in ['TEAM','W', 'L'] + selected_columns]
        data = df_filtered[['TEAM','W', 'L'] + selected_columns].to_dict('records')
        return columns, data
    
    @app.callback(
        [Output('Age', 'children'),
         Output('Points_Player', 'children'),
         Output('Reb_Player', 'children'),
         Output('Ast_Player', 'children'),
         Output('Blk_Player', 'children'),
         Output('Stl_Player', 'children'),
         Output('Tov_Player', 'children')],
        [Input('dropdown-season-player', 'value'),
         Input('button-all', 'n_clicks'),
         Input('button-guard', 'n_clicks'),
         Input('button-fordward', 'n_clicks'),
         Input('button-center', 'n_clicks')]
    )
    def update_counters_player(season, all_clicks, guard_clicks, forward_clicks, center_clicks):
 

        # Identificar qué botón fue presionado
        ctx = callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        # Determinar el filtro de posición según el botón presionado
        if button_id == 'button-all':
            filtered_position = None  # Sin filtro
        elif button_id == 'button-guard':
            filtered_position = 'Guard'
        elif button_id == 'button-forward':
            filtered_position = 'Fordward'
        elif button_id == 'button-center':
            filtered_position = 'Center'
        else:
            filtered_position = None  # Default si no hay botón presionado


        df_filtered = dfplayer[dfplayer['Season'] == season]

        if filtered_position:
            df_filtered = df_filtered[df_filtered['Position'] == filtered_position]

        age = df_filtered['Age'].mean().round(2)
        pts = (df_filtered['PTS'] / df_filtered['GP']).mean().round(2)
        reb = (df_filtered['REB'] / df_filtered['GP']).mean().round(2)
        ast = (df_filtered['AST'] / df_filtered['GP']).mean().round(2)
        blk = (df_filtered['BLK'] / df_filtered['GP']).mean().round(2)
        stl = (df_filtered['STL'] / df_filtered['GP']).mean().round(2)
        tov = (df_filtered['TOV'] / df_filtered['GP']).mean().round(2)

        
        
        return age, pts, reb, ast, blk, stl, tov
    
    @app.callback(
        Output('inner-tab-content-player', 'children'),
        [Input('inner-tabs-players', 'value')]
    )
    def render_inner_content_player(tab):
        if tab == 'graph-3':
            return dcc.Graph(id='bar-chart-player', style={'margin-top': '20px'})
        elif tab == 'graph-4':
            return dcc.Graph(id='box-chart-player',  style={'margin-top': '20px'})
    
    @app.callback(Output('bar-chart-player', 'figure'),[
                    Input('dropdown-season-player', 'value'),
                    Input('button-all', 'n_clicks'),
                    Input('button-guard', 'n_clicks'),
                    Input('button-fordward', 'n_clicks'),
                    Input('button-center', 'n_clicks')])
    def update_bar_shoting_player(season, all_clicks, guard_clicks, forward_clicks, center_clicks):
        # Identificar qué botón fue presionado
        ctx = callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        # Determinar el filtro de posición según el botón presionado
        if button_id == 'button-all':
            filtered_position = None 
        elif button_id == 'button-guard':
            filtered_position = 'Guard'
        elif button_id == 'button-forward':
            filtered_position = 'Fordward'
        elif button_id == 'button-center':
            filtered_position = 'Center'
        else:
            filtered_position = None  # Default si no hay botón presionado


        df_filtered = dfplayer[dfplayer['Season'] == season]

        if filtered_position:
            df_filtered = df_filtered[df_filtered['Position'] == filtered_position]
        
        averages         = df_filtered[['PTS2PT MR%', 'PTS3PT%', 'PTSFBPS%', 'PTSFT%', 'PTSPITP%' ]].mean().round(2).reset_index()
        averages.columns = ['Shooting Area', '% of Baskets Scored by Area']
        averages.loc[averages['Shooting Area'] == 'PTSPITP%', '% of Baskets Scored by Area'] -= averages.loc[averages['Shooting Area'] == 'PTSFBPS%', '% of Baskets Scored by Area'].values[0]

        averages['Shooting Area'] = averages['Shooting Area'].replace({
            'PTS2PT MR%': 'Midrange',
            'PTS3PT%': 'Three Points',
            'PTSFBPS%': 'Fast Break Points',
            'PTSFT%': 'Free Throws',
            'PTSPITP%': 'Points in the Paint'
        })

        averages = averages.sort_values(by='% of Baskets Scored by Area')
        

        # Crear un gráfico de barras con Plotly Express
        fig_bar_player = px.bar(averages, x='Shooting Area', y='% of Baskets Scored by Area',
                    title='',
                    color="Shooting Area",
                    color_discrete_sequence=custom_colors)

        fig_bar_player.update_layout(plot_bgcolor='white', 
                            yaxis_title='% of Baskets Scored by Area',
                            xaxis_title= '',
                            legend_title_text='Shooting Area')
        
        return fig_bar_player
    
    @app.callback(Output('box-chart-player', 'figure'),
                    Input('dropdown-season-player', 'value'))
    
    def update_box_pie_player(season):
        df_filtered = dfplayer[dfplayer['Season'] == season]
        bins        = [18, 25, 30, max(df_filtered.Age)]  # Limites de los grupos de edad
        labels      = ["Young Player (18-25)", "Mid-Age Player (26-30)", "Veteran Player (31 or more)"]  # Nombres de los grupos
        df_filtered['Age Group'] = pandas.cut(df_filtered['Age'], bins=bins, labels=labels, right=True)

        fig = px.box(
            df_filtered,
            x="Position",         
            y="PIE",              
            color="Age Group",    
            title="",
            color_discrete_sequence=custom_colors  
        )



        fig.update_layout(
            legend=dict(
                orientation="h",  # Cambia la orientación a horizontal
                yanchor="bottom",  # Ancla la leyenda en la parte inferior
                y=1.02,  # Posición vertical de la leyenda
                xanchor="center",  # Ancla la leyenda en el centro
                x=0.5  # Posición horizontal de la leyenda
            ),
            boxmode="group",          
            plot_bgcolor="white",     
            xaxis_title="Position",   
            yaxis_title="PIE (Player Impact Estimated)",        
            title_x=0.5               
        )

        return fig

    @app.callback(
    Output("tables-container", "children"),
    [
        Input("season-dropdown-1", "value"),
        Input("player-dropdown-1", "value"),
        Input("stats-dropdown-p1", "value"),
        Input("season-dropdown-2", "value"),
        Input("player-dropdown-2", "value"),
        Input("stats-dropdown-p2", "value"),
        Input("season-dropdown-3", "value"),
        Input("player-dropdown-3", "value"),
        Input("stats-dropdown-p3", "value"),
    ]
)
    def update_all_tables(season1, player1, stats1, season2, player2, stats2, season3, player3, stats3):
        tables = []  # Inicializa la lista de tablas
        inputs = [
            (season1, player1, stats1),
            (season2, player2, stats2),
            (season3, player3, stats3)
        ]

        for index, (season, player, stats) in enumerate(inputs):
            if season and player:  # Solo genera la tabla si ambos valores están seleccionados
                # Filtrar datos
                filtered_data = dfplayer[(dfplayer["Season"] == season) & (dfplayer["Player"] == player)]

                # Verifica que filtered_data no esté vacío
                if not filtered_data.empty:
                    # Tabla inicial con nombre del jugador
                    initial_data = [{"Var": "Player Name", "Observation": player}]

                    # Agregar variables seleccionadas
                    if stats:
                        for var in stats:
                            if var in filtered_data.columns:
                                initial_data.append({"Var": var, "Observation": filtered_data.iloc[0][var]})

                    # Crear la tabla
                    table = dash_table.DataTable(
                        id={"type": "dynamic-table", "index": f"table-{index}"},
                        columns=[{"name": "Var", "id": "Var"}, {"name": "Observation", "id": "Observation"}],
                        data=initial_data,
                        style_table={'width': '90%'},
                        style_cell={'textAlign': 'center',
                                    'font-family': 'Segoe UI',
                                    'backgroundColor': '#f9f9f9'},
                        style_header={
                            'backgroundColor': '#28334AFF',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_data={'backgroundColor': '#f9f9f9', 'color': 'black'}
                    )

                    # Contenedor para cada tabla y su dropdown
                    dropdown_and_table = html.Div([
                        table
                    ], style={"width": "30%", "text-align": "center"})

                    tables.append(dropdown_and_table)
                else:
                    # Si no hay datos, puedes mostrar un mensaje o una tabla vacía
                    tables.append(html.Div("No data available for the selected season and player.", style={"text-align": "center"}))
            else:
                tables.append(html.Div("", style={"text-align": "center"}))

        return tables

    @app.callback(
    [Output('player-dropdown-1', 'options'),
     Output('player-dropdown-1', 'value'),
     Output('player-dropdown-2', 'options'),
     Output('player-dropdown-2', 'value'),
     Output('player-dropdown-3', 'options'),
     Output('player-dropdown-3', 'value')],
    [Input('season-dropdown-1', 'value'),
     Input('season-dropdown-2', 'value'),
     Input('season-dropdown-3', 'value')]
)
    def actualizar_opciones_jugadores(season1, season2, season3):
        def obtener_jugadores(season):
            if season is None:
                return [], None  # Sin selección, retorna opciones vacías
            jugadores = dfplayer[dfplayer['Season'] == season]['Player'].unique()
            opciones = [{'label': jugador, 'value': jugador} for jugador in jugadores]
            valor_seleccionado = opciones[0]['value'] if opciones else None
            return opciones, valor_seleccionado

        opciones1, valor1 = obtener_jugadores(season1)
        opciones2, valor2 = obtener_jugadores(season2)
        opciones3, valor3 = obtener_jugadores(season3)

        return opciones1, valor1, opciones2, valor2, opciones3, valor3

    


    

