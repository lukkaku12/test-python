import pytest
from requests import get
from datetime import datetime, timedelta

class TestPriceApi:
    URL_BASE = "https://l2h237eh53.execute-api.us-east-1.amazonaws.com/dev/precios"
    
    def test_price_data(self):
        start = '2024-03-01'
        end = '2024-03-03'
        response = get(f'{self.URL_BASE}?start_date={start}&end_date={end}')
        
        assert response.status_code == 200
        
        data = response.json()
        
        assert isinstance(data, dict)
        assert 'data' in data
        assert 'total_days' in data
        assert 'message' in data
        assert isinstance(data['data'], dict)       
        
    def test_missing_parameters(self):
        """Test de parámetros faltantes"""
        # Test sin parámetros
        response = get(self.URL_BASE)
        assert response.status_code == 400
        assert "error" in response.json()
        data = response.json()
        assert data["error"] == "Se requiere start_date y end_date en los parámetros de consulta"
    
        # Test con solo un parámetro
        response = get(f'{self.URL_BASE}?start_date=2024-03-01')
        assert response.status_code == 400
        assert "error" in response.json()
        data = response.json()
        assert data["error"] == "Se requiere start_date y end_date en los parámetros de consulta"
    
    @pytest.mark.parametrize("start,end, expected_message", [
        ('2024/03/01', '2024-03-03', "Formato de fecha inválido. Usa YYYY-MM-DD"),
        ('2024-13-01', '2024-03-03', "Formato de fecha inválido. Usa YYYY-MM-DD"),
        ('2024-03-32', '2024-04-01', "Formato de fecha inválido. Usa YYYY-MM-DD"),
        ('invalid', '2024-03-03', "Formato de fecha inválido. Usa YYYY-MM-DD"),
    ])    
    
    def test_invalid_date_formats(self, start, end, expected_message):
        """Test de diferentes formatos inválidos de fecha"""
        response = get(
            self.URL_BASE,
            params={'start_date': start, 'end_date': end}
        )
        assert response.status_code == 400
        assert "error" in response.json()
        assert expected_message in response.json()["error"]
            
    def test_date_range_validation(self):
        """Test de validaciones de rango de fechas"""
        # Rango mayor a 30 días
        start = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')
        end = datetime.now().strftime('%Y-%m-%d')
        response = get(
            self.URL_BASE,
            params={'start_date': start, 'end_date': end}
        )
        assert response.status_code == 400
        assert "error" in response.json()
        assert "30 días" in response.json()["error"]
        
        # Fecha final anterior a la inicial
        start = datetime.now().strftime('%Y-%m-%d')
        end = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        response = get(
            self.URL_BASE,
            params={'start_date': start, 'end_date': end}
        )
        assert response.status_code == 400
        assert "error" in response.json()
        assert 'Fecha final debe ser mayor que la fecha de inicio' == response.json()["error"]