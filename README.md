# Prueba Técnica: Análisis de Precios de Energía

## 📋 Descripción del Proyecto
Sistema de análisis de precios de energía que obtiene datos de una API, realiza procesamiento estadístico y almacena los resultados en una base de datos SQLite.

## 🎯 Objetivos
- Obtener datos de precios energéticos vía API
- Procesar y limpiar datos temporales
- Calcular métricas estadísticas
- Visualizar tendencias de precios
- Almacenar resultados procesados

## 📚 Especificaciones de la API

### Endpoint
```
GET https://l2h237eh53.execute-api.us-east-1.amazonaws.com/dev/precios
```

### Parámetros
| Parámetro    | Tipo     | Descripción                    | Formato    |
|--------------|----------|--------------------------------|------------|
| `start_date` | string   | Fecha inicial de consulta      | YYYY-MM-DD |
| `end_date`   | string   | Fecha final de consulta        | YYYY-MM-DD |

### Ejemplo de Uso
```bash
curl "https://l2h237eh53.execute-api.us-east-1.amazonaws.com/dev/precios?start_date=2024-03-01&end_date=2024-03-10"
```

## 🔄 Flujo de Procesamiento

1. **Obtención de Datos (10 puntos)**
   - Se solicita información de precios de energía mediante una API.
   - La solicitud debe incluir los parámetros `start_date` y `end_date` para especificar el rango de fechas.
   - Puntos adicionales: Manejo de errores HTTP
   - ¿Cuántos días se obtienen de datos?

2. **Procesamiento de los Datos (20 puntos)**
   - Los datos se transforman a un `DataFrame` de Pandas para su posterior análisis.
   - Normalización de formato temporal
      ```python
      # Ejemplo de transformación
      df = df.reset_index()
      df = df.rename(columns={'index': 'hora'})
      df_long = pd.melt(df, id_vars=['hora'], var_name='fecha', value_name='precio')
    - Se deben manejar las fechas y horas correctamente, considerando que algunos valores de hora puedan estar mal formateados (por ejemplo, `24:00` en lugar de `00:00`). `hint: utilizar str.replace & pd.to_datetime`

3. **Tratamiento de Datos Faltantes (30 puntos)**
   - Se deben identificar y gestionar las horas faltantes en el conjunto de datos. Los valores faltantes deben llenarse:
     - Primero, rellenando los datos faltantes en las horas con el valor anterior más cercano disponible.
     - Luego, para los días faltantes, se deben rellenar utilizando el promedio de los 3 días previos y los 3 días posteriores a la fecha faltante.
     - ¿Cuáles son las horas donde hacen falta valores?

4. **Cálculos de Promedios (10 puntos)**
   - Se debe calcular el **promedio diario** de precios.
   - Además, calcular un **promedio móvil de 7 días** de los precios diarios.

5. **Visualización (15 puntos) **
   - Se debe generar una gráfica que compare los promedios diarios con el promedio móvil de 7 días.
   - La gráfica debe ser clara, con leyenda y título apropiados.
   - Almacenar la gráfica como image.png
   - ¿Cuál es el comportamiento del precio para el periodo?

6. **Almacenamiento de Resultados (15 puntos)**
   - Almacenar los resultados diarios (promedio diario y promedio móvil de 7 días) en una base de datos SQLite.
   - El esquema de la tabla debe incluir las columnas `fecha`, `precio_promedio`, `precio_7d`.

## 🔧 Requisitos Técnicos

- **Python 3.x**
- **Bibliotecas**:
  - `requests`
  - `pandas`
  - `matplotlib`
  - `sqlite3`

## 📁 Estructura del Proyecto

```plaintext
.
├── README.md
├── image.png (archivo generado con la imagen resultante)
├── precios.db (archivo generado con la base de datos SQLite)
└── script.py/ipynb (el script de Python que realiza todas las operaciones)