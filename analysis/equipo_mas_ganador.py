# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 18:22:23 2024

@author: Emiliano
"""
import pandas as pd
from inline_sql import sql, sql_val

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv

partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
#%%
#ejercicio 5.1.1
consultaSQL="""SELECT id_local,
CASE WHEN goles_local>goles_visitante
THEN 1
ELSE 0
END AS local_ganador
FROM partidos_liga
WHERE nombre_liga LIKE 'England%';
"""
ganados_por_local=sql^consultaSQL
#digo que si gana el local pones 1, sino 0
#%%
consultaSQL="""SELECT id_visitante,
CASE WHEN goles_local<goles_visitante
THEN 1
ELSE 0
END AS visitante_ganador
FROM partidos_liga
WHERE nombre_liga LIKE 'England%';
"""
ganados_por_visitante=sql^consultaSQL
#digo que si gana el visitante pones 1, sino 0
#%%
consultaSQL="""SELECT id_local, COUNT(*) AS cantidad_ganados_local
FROM ganados_por_local
WHERE local_ganador=1
GROUP BY id_local;"""
cantidad_local=sql^consultaSQL
#cuento cuanto gano local
#%%
consultaSQL="""SELECT id_visitante, COUNT(*) AS cantidad_ganados_visitante
FROM ganados_por_visitante
WHERE visitante_ganador=1
GROUP BY id_visitante;"""
cantidad_visitante=sql^consultaSQL
#cuento cuantos gano visitante
#%%
consultaSQL="""SELECT id_visitante AS equipo, cantidad_ganados_local,cantidad_ganados_visitante
FROM cantidad_local
INNER JOIN cantidad_visitante
ON id_visitante=id_local;
"""
equipo_cantidad_ganados=sql^consultaSQL
#doy el equipo y cuantos gano de local y cuantos de visitante
#%%
consultaSQL="""SELECT equipo,cantidad_ganados_local + cantidad_ganados_visitante AS total_ganados
FROM equipo_cantidad_ganados;
"""
total_de_ganados=sql^consultaSQL
#pongo el equipo y la cantidad de partidos que gano en total
#%%
consultaSQL="""SELECT equipo
FROM total_de_ganados
WHERE total_ganados = (
    SELECT MAX(total_ganados)
    FROM total_de_ganados
);"""

equipo_mas_ganador=sql^consultaSQL
#devuelvo el id del equipo mas ganador
#%%
consultaSQL="""SELECT nombre_equipo AS equipo_ganador
FROM equipos_buenos
INNER JOIN equipo_mas_ganador
ON equipo=id_equipo"""
gano=sql^consultaSQL
gano.to_csv("C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\gano.csv", index=False, encoding='utf-8')
#devuelvo el nombre del equipo mas ganador