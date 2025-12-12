# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:40:00 2024

@author:
"""

import pandas as pd
from inline_sql import sql, sql_val

carpeta = "/"

# Correcting the file extension to .csv
jugador = pd.read_csv(carpeta + "enunciado_jugadores.csv")
skills = pd.read_csv(carpeta + "enunciado_jugadores_atributos.csv")
equipos = pd.read_csv(carpeta + "enunciado_equipos.csv")
liga = pd.read_csv(carpeta + "enunciado_liga.csv")
paises = pd.read_csv(carpeta + "enunciado_paises.csv")
partidos = pd.read_csv(carpeta + "enunciado_partidos.csv")
#%%
consultaSQL = """
              SELECT DISTINCT name, country_id
              FROM liga;
              """
liga_buena = sql^ consultaSQL 
liga_buena.to_csv("\liga_buena.csv", index=False, encoding='utf-8')


#hacemos nueva tabla que tenga nombre de liga y el id del pais.
#%%
consultaSQL = """
              SELECT DISTINCT season AS temporada, 
              date AS fecha,  
              country_id AS id_pais, 
              match_api_id AS id_partido, 
              home_team_api_id AS id_local, 
              away_team_api_id AS id_visitante, 
              home_team_goal AS goles_local, 
              away_team_goal AS goles_visitante,
              FROM partidos
              """

partidos_buenos = sql^ consultaSQL


#tomamos todas las columnas hasta goles de visitante de partidos 
#y dejamos fuera todas las demas ya que son redundantes
#%%
consultaSQL = """
              SELECT DISTINCT 
              partidos_buenos.*,
              liga.name AS nombre_liga
              FROM partidos_buenos
              INNER JOIN liga
              ON partidos_buenos.id_pais = liga.country_id;
              """

partidos_liga = sql^ consultaSQL
partidos_liga.to_csv("partidos_liga.csv", index=False, encoding='utf-8')


#tomamos todos los atributos de partidos buenos y cuando pais.id es igual a country_id,
#se agrega el valor que corresponde a liga.name
#%%
consultaSQL = """
SELECT  name AS nombre_pais,id AS id_pais
FROM paises;
              """
paises_buenos=sql^consultaSQL
paises_buenos.to_csv("\paises_buenos.csv", index=False, encoding='utf-8')


#tradujimos a español los atributos
#%%
consultaSQL="""
SELECT team_api_id AS id_equipo,team_long_name AS nombre_equipo
from equipos;
"""

equipos_buenos=sql^consultaSQL
equipos_buenos.to_csv("\equipos_buenos.csv", index=False, encoding='utf-8')


#dejamos lo que nos interesaba de equipos y lo tradujimos al español
#%%
consultaSQL="""SELECT id_partido, id_local AS id_equipo
FROM partidos_buenos
UNION ALL
SELECT id_partido,id_visitante AS id_equipo
FROM partidos_buenos;
"""

juega= sql^consultaSQL
juega.to_csv("\juega.csv", index=False, encoding='utf-8')
#%%
consultaSQL="""SELECT season,home_team_api_id AS team_api_id, home_player_1 AS player_id
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_2
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_3
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_4
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_5
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_6
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_7
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_8
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_9
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_10
FROM partidos
UNION ALL
SELECT season,home_team_api_id, home_player_11
FROM partidos
UNION ALL
SELECT season,away_team_api_id AS team_api_id, away_player_1 AS player_id
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_2
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_3
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_4
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_5
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_6
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_7
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_8
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_9
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_10
FROM partidos
UNION ALL
SELECT season,away_team_api_id, away_player_11
FROM partidos;
"""
JUEGO=sql^consultaSQL
JUEGO = JUEGO.dropna(subset= 'player_id')
#%%
consultaSQL="""SELECT DISTINCT *
FROM JUEGO;
"""
plantel =sql^consultaSQL
plantel.to_csv("\plantel.csv", index=False, encoding='utf-8')
#%%
consultaSQL="""SELECT (*)
FROM skills"""
habilidades=sql^consultaSQL
habilidades.to_csv("\habilidades.csv", index=False, encoding='utf-8')
#%%
consultaSQL="""SELECT 
player_api_id AS id_jugador,
player_name AS nombre_jugador,
birthday AS fecha_nacimiento,
height AS altura,
weight AS peso
FROM jugador"""
jugador_bueno=sql^consultaSQL
jugador_bueno.to_csv("\jugador_bueno.csv", index=False, encoding='utf-8')
#%%
consultaSQL="""SELECT DISTINCT season AS fecha_temporada
FROM partidos"""
temporada=sql^consultaSQL

temporada.to_csv("\temporada.csv", index=False, encoding='utf-8')
