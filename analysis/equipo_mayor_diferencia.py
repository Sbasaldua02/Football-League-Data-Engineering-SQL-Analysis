# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:05:19 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv

partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
#%%
consultaSQL="""SELECT id_local, SUM(goles_local) - SUM(goles_visitante) AS diferencia_goles_locales
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_local;"""
diferencia_local=sql^consultaSQL
#saco la diferencia del local y visitante en local
#%%
consultaSQL="""SELECT id_visitante,SUM(goles_visitante)-SUM(goles_local) AS diferencia_goles_visitante
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_visitante;
"""
diferencia_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT id_local AS equipo,diferencia_goles_visitante + diferencia_goles_locales AS diferencia_total
FROM diferencia_local
INNER JOIN diferencia_visitante
ON id_local=id_visitante"""
diferencia_tot=sql^consultaSQL
#%%
consultaSQL="""SELECT equipo,diferencia_total
FROM diferencia_tot
WHERE diferencia_total = (
    SELECT MAX(diferencia_total)
    FROM diferencia_tot
);"""
maximo_de_diferencia=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo AS equipo_goleador
FROM equipos_buenos
INNER JOIN maximo_de_diferencia
ON equipo=id_equipo"""
equipo_mayor_diferencia=sql^consultaSQL