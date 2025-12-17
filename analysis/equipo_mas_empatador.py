# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 21:05:45 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv
partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
#%%
consultaSQL="""SELECT id_local,
CASE WHEN goles_local=goles_visitante
THEN 1
ELSE 0
END AS local_empata
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND temporada='2015/2016';
"""
empate_por_local=sql^consultaSQL
#digo que si empata el local pones 1, sino 0
#%%
consultaSQL="""SELECT id_visitante,
CASE WHEN goles_local=goles_visitante
THEN 1
ELSE 0
END AS visitante_empata
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND temporada='2015/2016';
"""
empate_por_visitante=sql^consultaSQL
#digo que si empata el visitante pones 1, sino 0
#%%
consultaSQL="""SELECT id_local, COUNT(*) AS cantidad_empate_local
FROM empate_por_local
WHERE local_empata=1
GROUP BY id_local;"""
cantidad_local=sql^consultaSQL
#cuento cuanto empata local
#%%
consultaSQL="""SELECT id_visitante, COUNT(*) AS cantidad_empate_visitante
FROM empate_por_visitante
WHERE visitante_empata=1
GROUP BY id_visitante;"""
cantidad_visitante=sql^consultaSQL
#cuento cuantos empata visitante
#%%
consultaSQL="""SELECT id_visitante AS equipo, cantidad_empate_local,cantidad_empate_visitante
FROM cantidad_local
INNER JOIN cantidad_visitante
ON id_visitante=id_local;
"""
equipo_cantidad_empate=sql^consultaSQL
#doy el equipo y cuantos empato de local y de visitante
#%%
consultaSQL="""SELECT equipo,cantidad_empate_local + cantidad_empate_visitante AS total_empate
FROM equipo_cantidad_empate;
"""
total_de_empate=sql^consultaSQL
#pongo el equipo y la cantidad de partidos que empato en total
#%%
consultaSQL="""SELECT equipo
FROM total_de_empate
WHERE total_empate = (
    SELECT MAX(total_empate)
    FROM total_de_empate
);
"""
equipo_mas_empatador=sql^consultaSQL
#devuelvo el id del equipo mas empatador
#%%
consultaSQL="""SELECT MIN(equipo) AS equipo
FROM equipo_mas_empatador
"""
equipo_empatador_sin_repes=sql^consultaSQL
#elijo el equipo con menor id
#%%
consultaSQL="""SELECT nombre_equipo AS equipo_empatador
FROM equipos_buenos
INNER JOIN equipo_empatador_sin_repes
ON equipo=id_equipo"""
empato=sql^consultaSQL
#devuelvo el nombre del equipo mas empatador