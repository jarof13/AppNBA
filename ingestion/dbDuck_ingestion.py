# ingestion/load_to_duckdb.py
import duckdb
import pandas as pd

# 1. Conectarse a DuckDB (si no existe el archivo, lo crea solo)
con = duckdb.connect("data/nba.duckdb")

# 2. Leer los Excel con pandas (esto ya sabés hacerlo)
df_teams  = pd.read_excel("BBDD_Player.xlsx")
df_players = pd.read_excel("BBDD.xlsx")

# 3. Crear un schema "bronze" para dejar claro que es data sin transformar
con.execute("CREATE SCHEMA IF NOT EXISTS bronze")  # pista: "CREATE SCHEMA IF NOT EXISTS raw"


# 4. Escribir cada DataFrame como tabla en DuckDB
# pista: duckdb puede registrar un dataframe y hacer INSERT directo
# investigá: con.execute("CREATE OR REPLACE TABLE raw.teams AS SELECT * FROM df_teams")

con.execute("CREATE OR REPLACE TABLE bronze.team AS SELECT * FROM df_teams")  # tabla de equipos
con.execute("CREATE OR REPLACE TABLE bronze.player AS SELECT * FROM df_players")  # tabla de jugadores

# 5. Verificar que funcionó
result = con.execute("SELECT COUNT(*) FROM bronze.team").fetchone()
print(f"Filas en bronze.team: {result[0]}")

con.close()