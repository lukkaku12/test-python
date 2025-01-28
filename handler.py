from typing import Tuple
import json
import csv
from datetime import datetime, timedelta
import os

def validate_dates(start_date:str, end_date:str,) -> Tuple[bool, str]:
    """Validate format of start and end dates
    & check if end date is greater than start date
    & limit the date range to 30 days
    """
    
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return False, "Formato de fecha inválido. Usa YYYY-MM-DD"
    
    if end_date < start_date:
        return False, "Fecha final debe ser mayor que la fecha de inicio"
    
    if end_date - start_date > timedelta(days=30):
        return False, "Rango de fecha no debe exceder los 30 días"
    
    return True, ""

def read_price_data(start_date:str, end_date:str):
    """Read price data from csv file
    & filter data based on start and end date
    & return dictionary with date: {hour: value} format
    """
    
    price_data = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Date'], "%Y-%m-%d")
            if start_date <= date <= end_date:
                hourly_values = {
                    f'{str(i).zfill(2)}:00': (
                        round(float(row[f'Values_Hour{str(i).zfill(2)}']), 2)
                        if row[f'Values_Hour{str(i).zfill(2)}'] not in (None, '')
                        else None
                    )
                    for i in range(1, 25)
                }
                price_data[row['Date']] = hourly_values
    
    return price_data

def handler(event, context):
    
    try:
        params = event.get('queryStringParameters', {})
        if not params or 'start_date' not in params or 'end_date' not in params:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Se requiere start_date y end_date en los parámetros de consulta'
                })
            }

        start_date = params["start_date"]
        end_date = params["end_date"]
        
        # Validate dates
        is_valid, error_message = validate_dates(start_date, end_date)
        if not is_valid:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': error_message
                })
            }
        
        # Read price data
        price_data = read_price_data(start_date, end_date)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Datos de precios recuperados exitosamente',
                'data': price_data,
                'total_days': len(price_data),
            })
        }
        
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error interno del servidor: {str(e)}'
            })
        }