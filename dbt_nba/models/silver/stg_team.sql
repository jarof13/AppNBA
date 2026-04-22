-- models/silver/stg_teams.sql

WITH source AS (
    SELECT * FROM bronze.teams
),

renamed AS (
    SELECT
        -- Columnas de identidad
        SEASON                          AS season,
        TEAM                            AS team_name,
        
        -- Columnas de performance 
        GP                              AS games_played,
        W                               AS wins,
        L                               AS losses,
        "WIN%"                          AS win_pct,
        MIN_x                           AS avg_minutes,
        MIN_y                           AS total_minutes,
        PTS                             AS points,
        FGM                             AS field_goals_made,
        FGA                             AS field_goals_attempted,
        "FG%"                           AS field_goals_pct,
        3PM                             AS three_field_goals_made,
        3PA                             AS three_field_goals_attempted,
        "3P%"                           AS three_field_goals_pct,
        FTM                             AS free_field_goals_made,
        FTA                             AS free_field_goals_attempted,
        "FT%"                           AS free_field_goals_attempted
        "FGA2PT%"                       AS pct
        "FGA3PT%"                       AS
        "PTS_2PT%"                      AS
        "PTS_2PT_MR%"                   AS
        "PTS_3PT%"                      AS
        "PTS_FBP%"                      AS
        "PTS_FT%"                       AS
        "PTS_OFFTO%"                    AS
        "PTS_PITP%"                     AS
        "2FGM_AST%"                     AS
        "2FGM_UAST%"                    AS
        "3FGM_AST%"                     AS
        "3FGM_UAST%"                    AS
        "FGM_AST%"                      AS
        "FGM_UAST%"                     AS
      

        -- Audit column
        CURRENT_TIMESTAMP               AS loaded_at

    FROM source
)

SELECT * FROM renamed