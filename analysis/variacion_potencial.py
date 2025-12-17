# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 18:29:12 2024

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
habilidades=pd.read_csv(carpeta + "habilidades.csv")

#%%
consultaSQL = """select player_api_id AS id_jugador, MIN(date) AS primer_año, MAX(date) AS ultimo_año
FROM habilidades
group by player_api_id;"""
primer_y_ultimo_año=sql^consultaSQL
#%%
consultaSQL="""SELECT id_jugador,primer_año,potential as potencial1
from primer_y_ultimo_año
INNER JOIN habilidades
ON date=primer_año;"""
primer_año=sql^consultaSQL
#%%

consultaSQL="""SELECT id_jugador,ultimo_año,potential as potencial2
from primer_y_ultimo_año
INNER JOIN habilidades
ON date=ultimo_año;"""
ultimo_año=sql^consultaSQL
#%%
consultaSQL="""SELECT id_jugador,ABS(potencial2 - potencial1) AS diferencia_potencial
from primer_año
INNER JOIN ultimo_año
WHERE primer_año.id_jugador=ultimo_año.id_jugador
group by id_jugador;"""
s=sql^consultaSQL
#%%
consultaSQL="""SELECT id_jugador,MIN(diferencia_potencial)
FROM s
GROUP BY id_jugador"""
t=sql^consultaSQL