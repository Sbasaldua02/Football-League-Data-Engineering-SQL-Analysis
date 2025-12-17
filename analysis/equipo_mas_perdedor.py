# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 20:33:38 2024

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
consultaSQL="""SELECT id_local,temporada,
CASE WHEN goles_local<goles_visitante
THEN 1
ELSE 0
END AS local_perdedor
FROM partidos_liga
WHERE nombre_liga LIKE 'England%';
"""
perdidos_por_local=sql^consultaSQL
#digo que si pierde el local pones 1, sino 0
#%%
consultaSQL="""SELECT id_visitante,temporada,
CASE WHEN goles_local>goles_visitante
THEN 1
ELSE 0
END AS visitante_perdedor
FROM partidos_liga
WHERE nombre_liga LIKE 'England%';
"""
perdidos_por_visitante=sql^consultaSQL
#digo que si pierde el visitante pones 1, sino 0
#%%
consultaSQL="""SELECT temporada,id_local, COUNT(*) AS cantidad_perdidos_local
FROM perdidos_por_local
WHERE local_perdedor=1
GROUP BY temporada,id_local;"""
cantidad_local=sql^consultaSQL
#cuento cuanto perdio local
#%%
consultaSQL="""SELECT temporada,id_visitante, COUNT(*) AS cantidad_perdidos_visitante
FROM perdidos_por_visitante
WHERE visitante_perdedor=1
GROUP BY temporada,id_visitante;"""
cantidad_visitante=sql^consultaSQL
#cuento cuantos perdio visitante
#%%
consultaSQL="""SELECT cantidad_visitante.temporada AS temporada,id_visitante AS equipo, cantidad_perdidos_local,cantidad_perdidos_visitante
FROM cantidad_local
INNER JOIN cantidad_visitante
ON id_visitante=id_local AND cantidad_visitante.temporada=cantidad_local.temporada ;
"""
equipo_cantidad_perdidos=sql^consultaSQL
#doy el equipo y cuantos perdio de local y cuantos de visitante
#%%
consultaSQL="""SELECT temporada,equipo,cantidad_perdidos_local + cantidad_perdidos_visitante AS total_perdidos
FROM equipo_cantidad_perdidos;
"""
total_de_perdidos=sql^consultaSQL
#pongo el equipo y la cantidad de partidos que perdio en total
#%%
consultaSQL="""SELECT equipo,temporada
FROM total_de_perdidos AS t
WHERE total_perdidos = (
    SELECT MAX(total_perdidos)
    FROM total_de_perdidos
    WHERE temporada=t.temporada
);
"""
equipo_mas_perdedor=sql^consultaSQL
#devuelvo el id del equipo mas perdedor
#%%
consultaSQL="""SELECT temporada,MIN(equipo) AS equipo
FROM equipo_mas_perdedor
GROUP BY temporada"""
equipo_perdedor_sin_repes=sql^consultaSQL
#elijo el equipo con menor id
#%%
consultaSQL="""SELECT temporada,nombre_equipo AS equipo_perdedor
FROM equipos_buenos
INNER JOIN equipo_perdedor_sin_repes
ON equipo=id_equipo"""
perdio=sql^consultaSQL
#devuelvo el nombre del equipo mas perdedor