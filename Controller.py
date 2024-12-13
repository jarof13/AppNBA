import openpyxl, pandas, re, numpy
import plotly.express as px
import plotly.graph_objects as go

def Group_By_Mean(df:pandas.DataFrame) -> pandas.DataFrame:
    dfSummary = df.    groupby('SEASON')[['PTS', 'FGM', 'FGA','FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB',
                                                'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'OFFRTG','DEFRTG', 'NETRG', 'AST%', 'AST/TO', 
                                                'ASTRATIO', 'OREB%', 'DREB%','REB%', 'TOV%', 'EFG%', 'TS%', 'PACE', 'PIE', 'POSS', 'FGA2PT%', 
                                                'FGA3PT%', 'PTS_2PT%', 'PTS_2PT_MR%', 'PTS_3PT%', 'PTS_FBP%', 'PTS_FT%', 'PTS_OFFTO%', 'PTS_PITP%', 
                                                '2FGM_AST%', '2FGM_UAST%', '3FGM_AST%', '3FGM_UAST%', 'FGM_AST%', 'FGM_UAST%']].mean().reset_index()
    dfSummary = dfSummary.round(2)
    dfSummary["Season"] = "Season " + dfSummary["SEASON"]

    return dfSummary



def update_table_data(selected_variables, season, player, current_data,dfplayer):
    if not season or not player:
        return current_data

    # Filtrar datos para la temporada y jugador seleccionado
    filtered_data = dfplayer[(dfplayer["Season"] == season) & (dfplayer["Player"] == player)]

    if filtered_data.empty:
        return [{"Var": "Error", "Observation": f"No data for {player} in {season}"}]

    # Datos iniciales: siempre mostrar el nombre del jugador
    data = [{"Var": "Player Name", "Observation": player}]

    # Agregar variables seleccionadas
    if selected_variables:
        for var in selected_variables:
            data.append({"Var": var, "Observation": filtered_data.iloc[0][var]})

    return data
