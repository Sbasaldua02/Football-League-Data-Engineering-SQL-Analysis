# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 18:22:23 2024

@author:
"""


from datetime import datetime
import pandas as pd
from inline_sql import sql, sql_val

carpeta = "\"

# Correcting the file extension to .csv

plantel=pd.read_csv(carpeta+"plantel.csv")
partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
temporada=pd.read_csv(carpeta + "temporada.csv")
enunciado_equipos=pd.read_csv(carpeta + "enunciado_equipos.csv")
jugador_bueno=pd.read_csv(carpeta+"jugador_bueno.csv")
partidos_buenos=pd.read_csv(carpeta + "partidos_buenos.csv")
habilidades=pd.read_csv(carpeta + "habilidades.csv")

#%%===========================================================================

# ¿CUÁL ES EL EQUIPO CON MAYOR CANTIDAD DE PARTIDOS GANADOS?

#=============================================================================
#%%
#ejercicio 5.1.1
consultaSQL="""SELECT id_local,
CASE WHEN goles_local>goles_visitante
THEN 1
ELSE 0
END AS local_ganador
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
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
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
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

#devuelvo el nombre del equipo mas ganador
#%%===========================================================================

# ¿CUÁL ES EL EQUIPO CON MAYOR CANTIDAD DE PARTIDOS PERDIDOS DE CADA AÑO?

#=============================================================================
#%%
consultaSQL="""SELECT id_local,temporada,
CASE WHEN goles_local<goles_visitante
THEN 1
ELSE 0
END AS local_perdedor
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
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
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012')) ;
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
#%%===========================================================================

# ¿CUÁL ES EL EQUIPO CON MAYOR CANTIDAD DE PARTIDOS EMPATADOS EN EL ÚLTIMO AÑO?

#=============================================================================
#%%
consultaSQL="""SELECT id_local,
CASE WHEN goles_local=goles_visitante
THEN 1
ELSE 0
END AS local_empata
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND temporada='2011/2012';
"""
empate_por_local=sql^consultaSQL
#digo que si empata el local pones 1, sino 0,tomamos temporada 2011/2012 porque es la ultima temporada de las que elegimos.
#%%
consultaSQL="""SELECT id_visitante,temporada,
CASE WHEN goles_local=goles_visitante
THEN 1
ELSE 0
END AS visitante_empata
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND temporada='2011/2012';
"""
empate_por_visitante=sql^consultaSQL
#digo que si empata el visitante pones 1, sino 0,tomamos temporada 2011/2012 porque es la ultima temporada de las que elegimos.
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
#devuelvo el nombre del equipo mas 
#%%===========================================================================

#  ¿CUÁL ES EL EQUIPO CON MAYOR CANTIDAD DE GOLES A FAVOR?

#=============================================================================
#%%
consultaSQL="""SELECT id_local,SUM(goles_local) AS suma_goles_locales
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'))
GROUP BY id_local"""
suma_local=sql^consultaSQL
#SUMO TODA LA CANTIDAD DE GOLES QUE TIENE CADA EQUIPO,JUGANDO COMO LOCAL
#%%
consultaSQL="""SELECT id_visitante,SUM(goles_visitante) AS suma_goles_visitante
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'))
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
#%%===========================================================================

#  ¿CUÁL ES EL EQUIPO CON MAYOR DIFERENCIA DE GOLES?

#=============================================================================
#%%
consultaSQL="""SELECT id_local, SUM(goles_local) - SUM(goles_visitante) AS diferencia_goles_locales
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'))
GROUP BY id_local;"""
diferencia_local=sql^consultaSQL
#saco la diferencia del local y visitante en local
#%%
consultaSQL="""SELECT id_visitante,SUM(goles_visitante)-SUM(goles_local) AS diferencia_goles_visitante
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'))
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
consultaSQL="""SELECT nombre_equipo AS equipo_con_mayor_diferencia_de_gol
FROM equipos_buenos
INNER JOIN maximo_de_diferencia
ON equipo=id_equipo"""
equipo_mayor_diferencia=sql^consultaSQL


#%%===========================================================================

#  ¿CUÁNTOS JUGADORES TUVO DURANTE EL PERÍODO DE TIEMPO SELECCIONADO CADA EQUIPO EN SU PLANTEL?

#=============================================================================

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

#%%===========================================================================

# ¿CUÁLES SON LOS JUGADORES QUE MÁS PARTIDOS GANÓ SU EQUIPO?

#=============================================================================
#%%
consultaSQL="""SELECT id_local,temporada,
CASE WHEN goles_local>goles_visitante
THEN 1
ELSE 0
END AS local_ganador
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
"""
ganados_por_local=sql^consultaSQL
#digo que si gana el local pones 1, sino 0
#%%
consultaSQL="""SELECT id_visitante,temporada,
CASE WHEN goles_local<goles_visitante
THEN 1
ELSE 0
END AS visitante_ganador
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' AND (temporada IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));
"""
ganados_por_visitante=sql^consultaSQL
#digo que si gana el visitante pones 1, sino 0
#%%
consultaSQL="""SELECT id_local, COUNT(*) AS cantidad_ganados_local,temporada
FROM ganados_por_local
WHERE local_ganador=1
GROUP BY id_local,temporada;"""
cantidad_local=sql^consultaSQL
#cuento cuanto gano local
#%%
consultaSQL="""SELECT id_visitante, COUNT(*) AS cantidad_ganados_visitante,temporada
FROM ganados_por_visitante
WHERE visitante_ganador=1
GROUP BY id_visitante,temporada"""
cantidad_visitante=sql^consultaSQL
#cuento cuantos gano visitante
#%%
consultaSQL="""SELECT id_visitante AS equipo, cantidad_ganados_local,cantidad_ganados_visitante,cantidad_visitante.temporada
FROM cantidad_local
INNER JOIN cantidad_visitante
ON id_visitante=id_local AND cantidad_visitante.temporada=cantidad_local.temporada;
"""
equipo_cantidad_ganados=sql^consultaSQL
#doy el equipo y cuantos gano de local y cuantos de visitante
#%%
consultaSQL="""SELECT equipo,cantidad_ganados_local + cantidad_ganados_visitante AS total_ganados,temporada
FROM equipo_cantidad_ganados;
"""
total_de_ganados=sql^consultaSQL
#pongo el equipo y la cantidad de partidos que gano en total
#%%
consultaSQL="""SELECT equipo,temporada
FROM total_de_ganados AS t
WHERE total_ganados = (
    SELECT MAX(total_ganados)
    FROM total_de_ganados
    WHERE temporada=t.temporada
);"""

equipo_mas_ganador=sql^consultaSQL
#devuelvo el id del equipo mas ganador
#%%
consultaSQL="""SELECT nombre_equipo AS equipo_ganador,temporada
FROM equipos_buenos
INNER JOIN equipo_mas_ganador
ON equipo=id_equipo"""
gano=sql^consultaSQL

#devuelvo el nombre del equipo mas ganador
#%%
consultaSQL="""SELECT id_equipo,temporada
FROM gano
INNER JOIN equipos_buenos
ON nombre_equipo=equipo_ganador"""
gano_id=sql^consultaSQL
#%%
consultaSQL="""SELECT id_equipo,temporada,player_id
FROM gano_id
INNER JOIN plantel
ON id_equipo=team_api_id AND temporada=season"""
jugadores_mas_ganadores=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,temporada,player_id
FROM jugadores_mas_ganadores
INNER JOIN equipos_buenos
ON jugadores_mas_ganadores.id_equipo=equipos_buenos.id_equipo"""
jugador_con_equipo_mas_ganador=sql^consultaSQL
jugador_con_equipo_mas_ganador.to_csv("C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\jugador_con_equipo_mas_ganador.csv", index=False, encoding='utf-8')
#%%===========================================================================

# ¿CUÁL ES EL JUGADOR QUE ESTUVO EN MÁS EQUIPOS?

#=============================================================================
#%%
consultaSQL="""SELECT season,team_api_id,player_id,nombre_equipo
FROM plantel
INNER JOIN equipos_buenos
ON team_api_id=id_equipo AND (season IN ('2008/2009', '2009/2010', '2010/2011', '2011/2012'));"""
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
jugador_con_mas_apariciones.to_csv("C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\jugador_con_mas_apariciones.csv", index=False, encoding='utf-8')
#%%===========================================================================

# ¿CUÁL ES EL JUGADOR QUE MENOR VARIACIÓN DE POTENCIA HA TENIDO A LO LARGO DE LOS AÑOS? (MEDIDA EN VALOR ABSOLUTO)

#=============================================================================
#%%
habilidades['date'] = pd.to_datetime(habilidades['date'])
consultaSQL = """ SELECT  player_api_id, potential, 
    CASE 
        WHEN MONTH(date) BETWEEN 1 AND 5 THEN YEAR(date) - 1
        ELSE YEAR(date)
    END AS año
FROM 
    habilidades;
"""
habilidades_año = sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
from habilidades_año
WHERE año IN (2008,2009,2010,2011)"""
habilidades_año=sql^consultaSQL
#%%
consultaSQL="""SELECT id_local AS id_equipo,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' 
GROUP by temporada,id_equipo"""
equipos_ingleses =sql^consultaSQL

#%%
consultaSQL="""SELECT (*)
FROM equipos_ingleses
WHERE temporada is not null"""
equipos_ingleses=sql^consultaSQL
#%%
consultaSQL ="""SELECT team_api_id, player_id,
CASE 
WHEN season LIKE '2008%' THEN 2008
WHEN season LIKE '2009%' THEN 2009
WHEN season LIKE '2010%' THEN 2010
WHEN season LIKE '2011%' THEN 2011
END AS temporada
FROM plantel
WHERE temporada is not null
GROUP by temporada,team_api_id,player_id"""
planteles_año =sql^consultaSQL
#%%
consultaSQL="""SELECT team_api_id,player_id,planteles_año.temporada
FROM planteles_año
INNER JOIN equipos_ingleses
ON team_api_id=id_equipo AND planteles_año.temporada=equipos_ingleses.temporada """
planteles_ingleses=sql^consultaSQL
#%%
consultaSQL = """ SELECT team_api_id, player_id, temporada, potential AS potencial
FROM planteles_ingleses
INNER JOIN habilidades_año
ON player_id =player_api_id and temporada = año
"""
planteles_potencial =sql^consultaSQL

#%%
consultaSQL = """SELECT temporada, MIN(potencial) AS potencial,player_id
FROM 
    planteles_potencial
GROUP BY temporada,player_id;
"""
planteles_potencial = sql^consultaSQL
#agarramos por año repetido el año con menor potencial del jugador.
#%%
consultaSQL="""SELECT player_id AS id_jugador, temporada AS primer_año, potencial AS potencial1
FROM planteles_potencial p1
WHERE temporada = (
    SELECT MIN(p2.temporada)
    FROM planteles_potencial p2
    WHERE p1.player_id = p2.player_id
)
GROUP BY player_id, temporada, potencial;
"""
primer_año=sql^consultaSQL
#lo que hacemos aca es agarrar jugador,temporada y potencial, cuando la temporada es igual a la minima temporada.
#%%

consultaSQL = """SELECT player_id AS id_jugador, temporada AS ultimo_año, potencial AS potencial2
FROM planteles_potencial p1
WHERE temporada = (
    SELECT MAX(p2.temporada)
    FROM planteles_potencial p2
    WHERE p1.player_id = p2.player_id
)
GROUP BY player_id, temporada, potencial;"""
ultimo_año=sql^consultaSQL

#%%
consultaSQL="""SELECT primer_año.id_jugador,ABS(potencial2 - potencial1) AS diferencia_potencial
from primer_año
INNER JOIN ultimo_año
ON primer_año.id_jugador=ultimo_año.id_jugador AND primer_año!=ultimo_año
group by primer_año.id_jugador,diferencia_potencial;"""
diferencia_potencial_año=sql^consultaSQL
#%%
consultaSQL="""SELECT id_jugador,diferencia_potencial AS menor_variacion_de_potencia
FROM diferencia_potencial_año p1
WHERE diferencia_potencial = (
    SELECT MIN(p2.diferencia_potencial)
    FROM diferencia_potencial_año p2
)
GROUP BY id_jugador, diferencia_potencial;"""
jugadores_con_menor_variacion=sql^consultaSQL
jugadores_con_menor_variacion.to_csv("C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\jugadores_con_menor_variacion.csv", index=False, encoding='utf-8')
#%%===========================================================================

# GRAFICAR LA CANTIDAD DE GOLES A FAVOR Y EN CONTRA DE CADA EQUIPO A LO LARGO DE LOS AÑOS QUE ELIJAN.

#=============================================================================
#%%
consultaSQL="""SELECT id_local,
SUM(goles_local) AS goles_a_favor,
SUM(goles_visitante) AS goles_en_contra,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP by temporada,id_local"""
goles_para_local=sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM goles_para_local
WHERE temporada is not null"""
temporada_sin_repes=sql^consultaSQL
#%%
consultaSQL = """
SELECT id_local,
       goles_a_favor,
       goles_en_contra,
       temporada
FROM temporada_sin_repes
WHERE id_local IN (
    SELECT id_local
    FROM temporada_sin_repes
    GROUP BY id_local
    HAVING COUNT(DISTINCT temporada) = 4
)
"""
cantidad_temporada_local = sql^consultaSQL



#%%
consultaSQL="""SELECT id_visitante,
SUM(goles_local) AS goles_en_contra,
SUM(goles_visitante) AS goles_a_favor,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP by temporada,id_visitante"""
goles_para_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM goles_para_visitante
WHERE temporada is not null"""
temporada_sin_repes_visita=sql^consultaSQL
#%%
consultaSQL = """
SELECT id_visitante,
       goles_a_favor,
       goles_en_contra,
       temporada
FROM temporada_sin_repes_visita
WHERE id_visitante IN (
    SELECT id_visitante
    FROM temporada_sin_repes_visita
    GROUP BY id_visitante
    HAVING COUNT(DISTINCT temporada) = 4
)
"""
cantidad_temporada_visitante = sql^consultaSQL

#%%
consultaSQL="""SELECT cantidad_temporada_visitante.temporada AS temporada,id_visitante AS id_equipo,cantidad_temporada_local.goles_a_favor+cantidad_temporada_visitante.goles_a_favor AS goles_favor,
cantidad_temporada_local.goles_en_contra + cantidad_temporada_visitante.goles_en_contra AS goles_contra
FROM cantidad_temporada_visitante
INNER JOIN cantidad_temporada_local
ON id_local=id_visitante AND cantidad_temporada_visitante.temporada=cantidad_temporada_local.temporada
ORDER BY temporada;
"""
goles_totales_s=sql^consultaSQL
#%%
consultaSQL="""SELECT temporada,team_short_name as nombre_equipo,goles_favor,goles_contra
FROM goles_totales_s
INNER JOIN enunciado_equipos
ON id_equipo=team_api_id"""
goles_totales=sql^consultaSQL
#%%

import matplotlib.pyplot as plt
import pandas as pd

color_favor = "#4A4063"
color_contra = "#BFACC8"

goles_totales['temporada'] = goles_totales['temporada'].astype(int)

goles_totales['equipo_temporada'] = goles_totales['nombre_equipo'].astype(str) + " - " + goles_totales['temporada'].astype(str)

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(goles_totales['equipo_temporada'], goles_totales['goles_favor'], 
       label='Goles a favor', color=color_favor)

ax.bar(goles_totales['equipo_temporada'], goles_totales['goles_contra'], 
       bottom=goles_totales['goles_favor'], label='Goles en contra', color=color_contra)


ax.set_title('Comparación de Goles a Favor y en Contra por Equipo y Temporada')

ax.set_xlabel('Equipo - Temporada')

ax.set_ylabel('Goles')

plt.xticks(rotation=90)  

plt.legend()

plt.tight_layout()

plt.show()
#%%===========================================================================

#GRAFICAR EL PROMEDIO DE GOL DE LOS EQUIPOS A LO LARGO DE LOS AÑOS QUE ELIJAN.

#===========================================================================
#%%
consultaSQL="""SELECT id_local,
COUNT(id_local) AS cantidad_partidos,
SUM(goles_local) AS goles_a_favor,
SUM(goles_visitante) AS goles_en_contra,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' 
GROUP by id_local,temporada;"""
cantidad_partidos_De_local=sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM cantidad_partidos_De_local
WHERE temporada is not null"""
cant_part_local_sin_repes=sql^consultaSQL
#%%
consultaSQL = """
SELECT id_local,
       goles_a_favor,
       cantidad_partidos,
       temporada
FROM cant_part_local_sin_repes
WHERE id_local IN (
    SELECT id_local
    FROM cant_part_local_sin_repes
    GROUP BY id_local
    HAVING COUNT(DISTINCT temporada) = 4
)
"""
cantidad_temporada_local_goles = sql^consultaSQL
#%%
consultaSQL="""SELECT id_visitante,
COUNT(id_visitante) AS cantidad_partidos,
SUM(goles_local) AS goles_en_contra,
SUM(goles_visitante) AS goles_a_favor,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' 
GROUP by id_visitante,temporada;"""
cantidad_partidos_De_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM cantidad_partidos_De_visitante
WHERE temporada is not null"""
cant_part_visitante_sin_repes=sql^consultaSQL
#%%
consultaSQL = """
SELECT id_visitante,
       goles_a_favor,
       cantidad_partidos,
       temporada
FROM cant_part_visitante_sin_repes
WHERE id_visitante IN (
    SELECT id_visitante
    FROM cant_part_visitante_sin_repes
    GROUP BY id_visitante
    HAVING COUNT(DISTINCT temporada) = 4
)
"""
cantidad_temporada_visitante_goles = sql^consultaSQL
#%%
consultaSQL = """
SELECT 
    id_visitante AS id_equipo,
    SUM(cantidad_temporada_visitante_goles.goles_a_favor) + SUM(cantidad_temporada_local_goles.goles_a_favor) AS goles,
    SUM(cantidad_temporada_visitante_goles.cantidad_partidos) + SUM(cantidad_temporada_local_goles.cantidad_partidos) AS cantidad_partidos,
    cantidad_temporada_visitante_goles.temporada AS temporada
FROM 
    cantidad_temporada_visitante_goles
INNER JOIN 
    cantidad_temporada_local_goles
ON 
    id_local = id_visitante AND cantidad_temporada_visitante_goles.temporada = cantidad_temporada_local_goles.temporada
GROUP BY 
    id_visitante, 
    cantidad_temporada_visitante_goles.temporada
ORDER BY 
    id_visitante;
"""
casi_promedio = sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,temporada,goles/cantidad_partidos as promedio_goles
FROM casi_promedio
INNER JOIN equipos_buenos
ON casi_promedio.id_equipo=equipos_buenos.id_equipo"""
promedio=sql^consultaSQL
#%%

import matplotlib.pyplot as plt
import numpy as np

colores = {
    2008: "#4A4063",
    2009: "#BFACC8",
    2010: "#7B4D79",
    2011: "#E0BBE4"
}

promedio['temporada'] = promedio['temporada'].astype(int)

promedio = promedio.sort_values(by=['nombre_equipo', 'temporada'])

fig, ax = plt.subplots(figsize=(10, 6))

equipos_unicos = promedio['nombre_equipo'].unique()
posiciones = np.arange(len(equipos_unicos))

bottom_values = np.zeros(len(equipos_unicos))

for temporada in colores.keys():
    
    datos_temporada = promedio[promedio['temporada'] == temporada]
    
    indices_equipos = [np.where(equipos_unicos == equipo)[0][0] for equipo in datos_temporada['nombre_equipo']]
    
    ax.bar(
        indices_equipos, 
        datos_temporada['promedio_goles'],  
        label=f'Temporada {temporada}',  
        color=colores[temporada],  
        bottom=bottom_values[indices_equipos] 
    )
    
    bottom_values[indices_equipos] += datos_temporada['promedio_goles'].values

ax.set_xticks(posiciones)
ax.set_xticklabels(equipos_unicos, rotation=90)

ax.set_title('Variación del promedio de goles por equipo y temporada')
ax.set_xlabel('Equipo')
ax.set_ylabel('Promedio de goles')
plt.legend()

plt.tight_layout()

plt.show()
#%%===========================================================================

#GRAFICAR LA DIFERENCIA DE GOLES CONVERTIDOS JUGANDO DE LOCAL VS VISITANTE A LO LARGO DEL TIEMPO.

#===========================================================================
#%%
consultaSQL="""SELECT id_local, SUM(goles_local) - SUM(goles_visitante) AS diferencia_goles_locales,temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_local,temporada;"""
diferencia_local=sql^consultaSQL
#%%
#saco la diferencia del local y visitante en local
consultaSQL="""SELECT id_visitante,SUM(goles_visitante)-SUM(goles_local) AS diferencia_goles_visitante,temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP BY id_visitante,temporada;
"""
diferencia_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT id_local AS equipo,diferencia_goles_visitante,diferencia_goles_locales,diferencia_visitante.temporada AS temporada
FROM diferencia_local
INNER JOIN diferencia_visitante
ON id_local=id_visitante AND diferencia_local.temporada=diferencia_visitante.temporada;"""
diferencia_tot=sql^consultaSQL
#%%
consultaSQL="""SELECT equipo,temporada,team_short_name as nombre_equipo,diferencia_goles_locales,diferencia_goles_visitante
FROM diferencia_tot
INNER JOIN enunciado_equipos
ON equipo=team_api_id"""
diferencia_tot=sql^consultaSQL
#%%
diferencia_tot['temporada'] = diferencia_tot['temporada'].str.split('/').str[0].astype(int)

#paso los datos de temporada a un solo año en tipo int
#%%
consultaSQL="""SELECT (*)
FROM diferencia_tot
WHERE temporada IN (2008,2009,2010,2011)"""
goles_para_local=sql^consultaSQL
#%%
consultaSQL="""SELECT equipo,
        nombre_equipo,
       diferencia_goles_locales,
       diferencia_goles_visitante,
       temporada
FROM goles_para_local
WHERE equipo IN (
    SELECT equipo
    FROM goles_para_local
    GROUP BY equipo
    HAVING COUNT(DISTINCT temporada) = 4
)"""
diferencia_tot=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,ABS(diferencia_goles_locales) AS diferencia_goles_locales,
ABS(diferencia_goles_visitante) AS diferencia_goles_visitante,temporada
FROM diferencia_tot"""
diferencia_tot=sql^consultaSQL
#%%
color_dif_local = "#4A4063"
color_dif_visitante = "#BFACC8"

diferencia_tot['temporada'] = diferencia_tot['temporada'].astype(int)

diferencia_tot['equipo_temporada'] = diferencia_tot['nombre_equipo'].astype(str) + " - " + diferencia_tot['temporada'].astype(str)

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(diferencia_tot['equipo_temporada'], diferencia_tot['diferencia_goles_locales'], 
       label='Diferencia de gol local', color=color_dif_local)

ax.bar(diferencia_tot['equipo_temporada'], diferencia_tot['diferencia_goles_visitante'], 
       bottom=diferencia_tot['diferencia_goles_locales'], label='Diferencia de gol visitante', color=color_dif_visitante)


ax.set_title('Comparación de diferencia de goles como local y visitante por Temporada')

ax.set_xlabel('Equipo - Temporada')

ax.set_ylabel('Goles')

plt.xticks(rotation=90)  

plt.legend()

plt.tight_layout()

plt.show()
#%%===========================================================================

#GRAFICAR EL NÚMERO DE GOLES CONVERTIDOS POR CADA EQUIPO EN FUNCIÓN DE LA SUMA DE TODOS SUS ATRIBUTOS.

#===========================================================================
#%%
habilidades['date'] = pd.to_datetime(habilidades['date'])
consultaSQL = """ SELECT  player_api_id, potential, overall_rating,finishing,dribbling,free_kick_accuracy,ball_control,acceleration,sprint_speed,agility,
shot_power, penalties,
    CASE 
        WHEN MONTH(date) BETWEEN 1 AND 5 THEN YEAR(date) - 1
        ELSE YEAR(date)
    END AS año
FROM 
    habilidades;
"""
habilidades_año = sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
from habilidades_año
WHERE año IN (2008,2009,2010,2011)"""
habilidades_año=sql^consultaSQL
#%%
consultaSQL="""SELECT id_local AS id_equipo,
CASE 
WHEN temporada LIKE '2008%' THEN 2008
WHEN temporada LIKE '2009%' THEN 2009
WHEN temporada LIKE '2010%' THEN 2010
WHEN temporada LIKE '2011%' THEN 2011
END AS temporada
FROM partidos_liga
WHERE nombre_liga LIKE 'England%' 
GROUP by temporada,id_equipo"""
equipos_ingleses =sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM equipos_ingleses
WHERE temporada is not null"""
equipos_ingleses=sql^consultaSQL
#%%
consultaSQL="""SELECT (*)
FROM equipos_ingleses
WHERE id_equipo IN (
    SELECT id_equipo
    FROM equipos_ingleses
    GROUP BY id_equipo
    HAVING COUNT(DISTINCT temporada) = 4
)"""
equipos_ingleses=sql^consultaSQL
#%%
consultaSQL ="""SELECT team_api_id, player_id,
CASE 
WHEN season LIKE '2008%' THEN 2008
WHEN season LIKE '2009%' THEN 2009
WHEN season LIKE '2010%' THEN 2010
WHEN season LIKE '2011%' THEN 2011
END AS temporada
FROM plantel
WHERE temporada is not null
GROUP by temporada,team_api_id,player_id"""
planteles_año =sql^consultaSQL
#%%
consultaSQL="""SELECT team_api_id,player_id,planteles_año.temporada
FROM planteles_año
INNER JOIN equipos_ingleses
ON team_api_id=id_equipo AND planteles_año.temporada=equipos_ingleses.temporada """
planteles_ingleses=sql^consultaSQL
#%%
consultaSQL = """ SELECT team_api_id, player_id, temporada, potential AS potencial,
overall_rating,finishing,dribbling,free_kick_accuracy,ball_control,acceleration,sprint_speed,agility,
shot_power, penalties
FROM planteles_ingleses
INNER JOIN habilidades_año
ON player_id =player_api_id and temporada = año;
"""
planteles_potencial =sql^consultaSQL
#%%
consultaSQL = """SELECT team_api_id,temporada, MIN(potencial) AS potencial,player_id,MIN(overall_rating) AS overall_rating,MIN(finishing) AS finishing,
MIN(dribbling) AS dribbling,MIN(free_kick_accuracy) AS free_kick_accuracy,MIN(ball_control) ball_control,MIN(acceleration) AS acceleration,MIN(sprint_speed) AS sprint_speed,MIN(agility) AS agility,
MIN(shot_power) AS shot_power, MIN(penalties) AS penalties 
FROM 
    planteles_potencial
GROUP BY team_api_id,temporada,player_id;
"""
planteles_atributos = sql^consultaSQL
#agarramos por año repetido el año con menor potencial del jugador.
#%%
consultaSQL="""SELECT player_id,team_api_id,potencial+
overall_rating+finishing+dribbling+free_kick_accuracy+ball_control+acceleration+sprint_speed+agility+
shot_power+ penalties AS suma_atributos
FROM planteles_atributos"""
suma_atributos=sql^consultaSQL
#%%
consultaSQL="""SELECT team_api_id,SUM(suma_atributos) AS suma_atributos
FROM suma_atributos
GROUP BY team_api_id"""
equipo_atributos=sql^consultaSQL
#%%
consultaSQL="""SELECT team_short_name AS nombre_equip,suma_atributos
FROM equipo_atributos
INNER JOIN enunciado_equipos
ON equipo_atributos.team_api_id=enunciado_equipos.team_api_id"""
nuevo_equipo_atributos=sql^consultaSQL
#%%
consultaSQL="""SELECT temporada,nombre_equipo,goles_favor+goles_contra as goles_totales
FROM goles_totales"""
nuevo_goles_totales=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,SUM(goles_totales) AS goles_totales
FROM nuevo_goles_totales
GROUP BY nombre_equipo"""
goles_totales_equipo=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,goles_totales,suma_atributos
FROM goles_totales_equipo
INNER JOIN nuevo_equipo_atributos
ON nombre_equipo=nombre_equip"""
goles_totales_equipo_atributos=sql^consultaSQL
#%%
consultaSQL="""SELECT team_short_name AS nombre_equip,cantidad_jugadores
FROM cantidad_jugadores_plantel
INNER JOIN enunciado_equipos
ON nombre_equipo=team_long_name"""
cantidad_jugadores_tot=sql^consultaSQL
#%%
consultaSQL="""SELECT nombre_equipo,goles_totales,suma_atributos/cantidad_jugadores AS suma_atributos
FROM goles_totales_equipo_atributos
INNER JOIN cantidad_jugadores_tot
ON nombre_equipo=nombre_equip"""
jugadores_atributos_goles=sql^consultaSQL
#%%

import numpy as np
import matplotlib.pyplot as plt


jugadores_atributos_goles_sorted = jugadores_atributos_goles.sort_values(by='suma_atributos')


jugadores_atributos_goles_sorted['atributos_equipo'] = (
    jugadores_atributos_goles_sorted['suma_atributos'].map('{:.1f}'.format) +  
    ' - ' + 
    jugadores_atributos_goles_sorted['nombre_equipo']
)


fig, ax = plt.subplots()


plt.rcParams['font.family'] = 'sans-serif'


ax.scatter(jugadores_atributos_goles_sorted['atributos_equipo'],  
           jugadores_atributos_goles_sorted['goles_totales'],     
           s=8,  
           color='magenta')  


ax.set_title('Relación entre atributos y goles por equipo')
ax.set_xlabel('Suma Atributos - Equipo', fontsize='medium')
ax.set_ylabel('Goles Totales', fontsize='medium')

# Colocar las etiquetas personalizadas en el eje X
ax.set_xticks(np.arange(len(jugadores_atributos_goles_sorted)))  
ax.set_xticklabels(jugadores_atributos_goles_sorted['atributos_equipo'], rotation=45, ha="right")  


plt.tight_layout()
plt.show()



