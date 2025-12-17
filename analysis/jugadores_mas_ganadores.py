# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:10:32 2024

@author: Emiliano
"""
import pandas as pd
from inline_sql import sql, sql_val
carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"
# Correcting the file extension to .csv
gano=pd.read_csv(carpeta+"gano.csv")
plantel=pd.read_csv(carpeta+"plantel.csv")
equipos_buenos=pd.read_csv(carpeta+"equipos_buenos.csv")
jugador_bueno=pd.read_csv(carpeta+"jugador_bueno.csv")
#%%
consultaSQL="""SELECT season,team_api_id,player_id,nombre_equipo
FROM plantel
INNER JOIN equipos_buenos
ON team_api_id=id_equipo"""
equipo_completo=sql^consultaSQL
#%%
consultaSQL="""SELECT DISTINCT player_id 
FROM equipo_completo
INNER JOIN gano
ON equipo_ganador=nombre_equipo"""
jugadores_mas_ganadores=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_jugador 
FROM jugador_bueno
INNER JOIN jugadores_mas_ganadores
ON id_jugador=player_id"""
nombre_jugadores_mas_ganadores=sql^consultaSQL