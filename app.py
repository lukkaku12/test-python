import requests
from pandas import DataFrame
import sqlite3


try:
    response = requests.get('https://l2h237eh53.execute-api.us-east-1.amazonaws.com/dev/precios?start_date=2024-03-15&end_date=2024-04-14').json()
    energy_prices = response['data']
    energy_prices_Df = DataFrame(energy_prices)
    energy_prices_Df

    #cuantos dias de datos?

    len(energy_prices_Df.columns)

    # reemplazar indices de 24:00 a 00:00

    energy_prices_Df.index = energy_prices_Df.index.str.replace('24:00', '00:00')
    energy_prices_Df

    # obtener columnas que estan nulas

    for colName in energy_prices_Df.columns:
        print(energy_prices_Df[colName][energy_prices_Df[colName].isnull()])

    # reemplazar numeros nulos

    energy_prices_Df.loc['15:00', '2024-04-08'] = energy_prices_Df.loc['14:00', '2024-04-08']
    
    # promedio diario de precios

    promedio_diario = energy_prices_Df.mean()


    conn = sqlite3.connect("precios.db")


    promedio_diario.to_sql('promedio_diario', conn)

    conn.close()



except Exception as e:
    print(e)