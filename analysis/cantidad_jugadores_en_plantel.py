# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:39:06 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv
partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
plantel=pd.read_csv(carpeta+ "plantel.csv")
#%%
consultaSQL="""SELECT season, team_api_id , player_id ,nombre_liga
FROM plantel
INNER JOIN partidos_liga
ON (season=temporada) AND (team_api_id=id_local) AND (nombre_liga LIKE 'England%')
AND (season IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
 """
plantel_temporadas=sql^consultaSQL 
#consideramos los jugadores que jugaron en la liga inglesa, en esos 4 años. 
#vimos la diferencia si tomamos todas las temporadas y con solo estas 4, el resultado nos da que hay equipos que ascendieron despues de 2012.
#lo que hacemos es agarrar los equipos y los jugadores que jugaron entre 2008 y 2012 en la liga inglesa.
#suponemos que todos los equipos jugaron al menos un partido de local.
#la eleccion de los años esta bien porque de 32 equipos totales, 27 estan en las temporadas 2008 y es mayor al 80%.
#%%
consultaSQL="""SELECT DISTINCT *
FROM plantel_temporadas;"""
plantel_temporadas_sin_repes=sql^consultaSQL
#sacamos tuplas repetidas.
#%%
consultaSQL="""SELECT team_api_id AS equipo,COUNT(player_id) AS cantidad_jugadores
FROM plantel_temporadas_sin_repes
GROUP BY equipo;"""
cantidad_jugadores_temporadas=sql^consultaSQL
#contamos cantidad de jugadores de cada equipo
#%%
consultaSQL="""SELECT nombre_equipo,cantidad_jugadores
FROM equipos_buenos
INNER JOIN cantidad_jugadores_temporadas
ON equipo=id_equipo"""
cantidad_jugadores_plantel=sql^consultaSQL
#cambiamos el id del equipo por el nombre