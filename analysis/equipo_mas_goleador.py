# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:15:59 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv

partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
#%%
consultaSQL="""SELECT id_local,SUM(goles_local) AS suma_goles_locales
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_local"""
suma_local=sql^consultaSQL
#SUMO TODA LA CANTIDAD DE GOLES QUE TIENE CADA EQUIPO,JUGANDO COMO LOCAL
#%%
consultaSQL="""SELECT id_visitante,SUM(goles_visitante) AS suma_goles_visitante
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_visitante"""
suma_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT id_local AS equipo,suma_goles_visitante + suma_goles_locales AS total_goles
FROM suma_local
INNER JOIN suma_visitante
ON id_local=id_visitante"""
suma_total=sql^consultaSQL
#%%
consultaSQL="""SELECT equipo,total_goles
FROM suma_total
WHERE total_goles = (
    SELECT MAX(total_goles)
    FROM suma_total
);"""
maximo_de_goles=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo AS equipo_goleador
FROM equipos_buenos
INNER JOIN maximo_de_goles
ON equipo=id_equipo"""
equipo_mas_goleador=sql^consultaSQL