# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 19:05:34 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val
carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"
# Correcting the file extension to .csv

plantel=pd.read_csv(carpeta+"plantel.csv")
equipos_buenos=pd.read_csv(carpeta+"equipos_buenos.csv")
jugador_bueno=pd.read_csv(carpeta+"jugador_bueno.csv")
partidos_buenos=pd.read_csv(carpeta + "partidos_buenos.csv")

#%%
consultaSQL="""SELECT season,team_api_id,player_id,nombre_equipo
FROM plantel
INNER JOIN equipos_buenos
ON team_api_id=id_equipo;"""
equipo_completo=sql^consultaSQL
#%%
consultaSQL="""SELECT DISTINCT team_api_id,player_id,nombre_equipo AS nombre_e
FROM equipo_completo;"""
jugadores=sql^consultaSQL
#%%
consultaSQL="""SELECT DISTINCT team_api_id,player_id,nombre_e
FROM jugadores
INNER JOIN partidos_buenos
ON id_local=team_api_id AND nombre_liga LIKE 'England%';"""
jugadores_inglaterra=sql^consultaSQL
#%%
consultaSQL="""SELECT player_id, COUNT(*) AS cantidad_equipos
FROM jugadores_inglaterra
GROUP BY player_id;"""
cantidad_jugadores=sql^consultaSQL
#%%
consultaSQL="""SELECT player_id, cantidad_equipos
FROM cantidad_jugadores
WHERE cantidad_equipos=(SELECT MAX(cantidad_equipos)
                       FROM cantidad_jugadores);"""
maxima_aparicion=sql^consultaSQL
#%%
consultaSQL="""SELECT MAX(player_id) AS jugador
FROM maxima_aparicion;
"""
jugador_buen=sql^consultaSQL
#elijo el que tiene maximo id
#%%
consultaSQL="""SELECT nombre_jugador 
FROM jugador_buen
INNER JOIN jugador_bueno
ON id_jugador=jugador;"""
jugador_con_mas_apariciones=sql^consultaSQL
