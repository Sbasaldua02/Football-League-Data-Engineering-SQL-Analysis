# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 19:50:20 2024

@author: Emiliano
"""

import pandas as pd
from inline_sql import sql, sql_val
import matplotlib.pyplot as plt # Para graficar series multiples
from   matplotlib import ticker   # Para agregar separador de miles
import seaborn as sns           # Para graficar histograma

carpeta = "C:\\Users\\segov\\OneDrive\\Escritorio\\enunciado_tablas\\"

# Correcting the file extension to .csv

partidos_liga=pd.read_csv(carpeta + "partidos_liga.csv")
equipos_buenos=pd.read_csv(carpeta + "equipos_buenos.csv")
#%%
consultaSQL="""SELECT temporada,id_local,SUM(goles_local) AS goles_a_favor,SUM(goles_visitante) AS goles_en_contra
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP by temporada,id_local"""
goles_para_local=sql^consultaSQL
#%%
consultaSQL="""SELECT temporada,id_visitante,SUM(goles_local) AS goles_en_contra,SUM(goles_visitante) AS goles_a_favor
FROM partidos_liga
WHERE nombre_liga LIKE 'England%'
GROUP by temporada,id_visitante"""
goles_para_visitante=sql^consultaSQL
#%%
consultaSQL="""SELECT goles_para_visitante.temporada AS temp,id_visitante AS id_equipo,goles_para_local.goles_a_favor+goles_para_visitante.goles_a_favor AS goles_favor,
goles_para_local.goles_en_contra + goles_para_visitante.goles_en_contra AS goles_contra
FROM goles_para_visitante
INNER JOIN goles_para_local
ON id_local=id_visitante AND goles_para_visitante.temporada=goles_para_local.temporada;
"""
goles_totales=sql^consultaSQL
#%%
#genero grafico
#%% 
# Genero gráfico
# Configuración de la fuente
# Convertir el rango a tipo fecha (tomar el primer año)
# goles_totales['temp'] = pd.to_datetime(goles_totales['temp'].str.split('/').str[0] + '-01-01')
plt.rcParams['font.family'] = 'sans-serif'

# Crear la figura y los ejes
fig, ax = plt.subplots()

# Graficar goles a favor
ax.plot(goles_totales['temp'], goles_totales['goles_favor'],
        marker='.',
        linestyle='-',
        linewidth=0.5,
        label='Goles a Favor')

# Graficar goles en contra
ax.plot(goles_totales['temp'], goles_totales['goles_contra'],
        marker='.',
        linestyle='-',
        linewidth=0.5,
        label='Goles en Contra')

rango_fechas = pd.date_range(start='2008-01-01', end='2016-12-31', freq='Y')
# Configurar títulos y etiquetas
ax.set_title('Cant. Goles a Favor y en Contra')  
ax.set_xlabel('Años')  
ax.set_ylabel('Cantidad Goles')  
ax.set_xticks(rango_fechas)  # Incluye el 2016
ax.set_yticks(range(0, 150, 10))

# Mostrar leyenda
ax.legend()

# Mostrar el gráfico
plt.show()
#%%
# # Genero gráfico
# fig, ax = plt.subplots()
# plt.rcParams['font.family'] = 'sans-serif'

# ax.plot(goles_totales['temp'], goles_totales['goles_favor'],
#         marker='.',
#         linestyle='-',
#         linewidth=0.5,
#         label='Goles a Favor')

# ax.plot(goles_totales['temp'], goles_totales['goles_contra'],
#         marker='.',
#         linestyle='-',
#         linewidth=0.5,
#         label='Goles en Contra')

# ax.set_title('Cant. Goles a favor y en contra', fontsize='large')  # Cambiado a set_title
# ax.set_xlabel('Años', fontsize='medium')  # Corregido fontsize
# ax.set_ylabel('Cantidad Goles', fontsize='medium')  # Corregido fontsize
# # ax.set_xticks(range(2008, 2016, 1))  # Cambiado a set_xticks
# ax.set_yticks(range(10, 150, 10))  # Cambiado a set_yticks

# ax.legend()  # Asegurarse de llamar al método

# plt.show()

