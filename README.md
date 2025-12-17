# Diseño de Base de Datos y Análisis de Rendimiento en Ligas de Fútbol
# Integrantes: Santos Basaldúa, Emiliano Segovia y Solana Sabor Schvartz

> **Ingeniería de Datos y Análisis de Ligas de Fútbol: Realizamos un Proceso ETL completo desde datos crudos a Modelo Relacional (3FN),  hicimos un análisis de rendimiento usando Python, pandas y consultas SQL.  Utilizamos herramientas de Visualización de datos (Matplotlib) para insights deportivos.**

Este proyecto ejemplifica el ciclo completo del dato, desde la ingeniería y modelado de datos crudos hasta la obtención de informacion de rendimiento. El foco fue transformar datasets iniciales (con redundancia y problemas de estructura) en una base de datos relacional optimizada para análisis deportivo.

---

## 1. Desafío y Metodología (Criterio Analítico)

Nuestro objetivo principal fue establecer una base de datos robusta para analizar el rendimiento de equipos y jugadores a lo largo de varias temporadas.

### Criterios Aplicados
Para garantizar la fiabilidad del análisis longitudinal, establecimos un criterio de selección estricto:

* **Ventana Temporal:** Seleccionamos **cuatro temporadas consecutivas** para evaluar la constancia en el rendimiento.
* **Estabilidad de Datos:** Solo incluimos **equipos que lograron mantener la categoría** (no descendieron) durante las temporadas analizadas. Esto minimiza la variación estadística ("ruido") introducida por equipos con ciclos de vida cortos en la liga.

---

## 2. Ingeniería y Modelado de Datos (ETL)

Nuestro primer paso fue aplicar conceptos de teoría de bases de datos para normalizar la información y asegurar su calidad.

### Arquitectura Relacional (3FN)
1.  **Diseño Conceptual:** Definimos un Diagrama Entidad-Relación (DER) para mapear las interrelaciones entre entidades clave (Jugador, Equipo, Partido, Habilidad).
2.  **Normalización a 3FN:** El modelo relacional que diseñamos fue validado para cumplir con la **Tercera Forma Normal (3FN)**, eliminando dependencias transitivas y asegurando la integridad referencial.
    * *Ver carpeta `docs/` para el diagrama DER y el modelo relacional.*
      <img width="634" height="463" alt="image" src="https://github.com/user-attachments/assets/e0a70980-516a-43fd-adfe-c4add580df67" />


### Scripts de Transformación (Python/Pandas/SQL)
* **`generar_tablas.py`:** Script en Python que ejecuta el proceso de Extracción y Transformación (ETL).
* **Transformación Relacional:** Realizamos consultas SQL de definición y manipulación (`SELECT DISTINCT`, `JOINs`) para descomponer datasets planos en entidades normalizadas, asignando claves foráneas y eliminando redundancias.

---

## 3. Análisis y Descubrimiento (SQL y Visualización)

Una vez que normalizamos la base de datos, aplicamos consultas SQL para extraer insights clave y la librería Matplotlib para su visualización.

### Consultas SQL Estructuradas
El script `analisis.py` contiene consultas específicas que demuestran el manejo de lógica relacional compleja:

* **Integración de Datos:** Uso de `INNER JOIN` para vincular rendimiento individual (goles, atributos) con resultados de equipo.
* **Lógica Condicional:** Implementación de `CASE WHEN` para clasificar resultados de partidos.
* **Agregación:** Métricas de resumen (`GROUP BY`, promedios) para evaluar el potencial de los jugadores.

### Visualización
Generamos gráficos utilizando **Matplotlib** para responder preguntas como:
* Relación entre atributos técnicos y goles anotados por equipo.
* Variación de la característica "potencial" en jugadores top a lo largo del tiempo.
* Dejo como ejemplo uno de los graficos obtenidos:
  <img width="957" height="442" alt="image" src="https://github.com/user-attachments/assets/ac3a8c5d-dc6f-4e5b-bd32-7a7a4b06e3b7" />


### Tecnologías Utilizadas
* **Lenguajes:** Python 3, SQL.
* **Librerías:** Pandas, NumPy, Matplotlib, `inline_sql`.
* **Conceptos:** ETL, Modelado de Datos, Normalización (3FN), tecnicas de Visualizacion de Datos.

---

**[Documentación Completa]**
*Pueden ver el informe detallado con las respuestas a las consignas en el archivo `docs/Informe.pdf`.*
