import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

class OpenMeteoAPI:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.latitude = -30.0331  # Porto Alegre
        self.longitude = -51.2300
        self.timezone = "America/Sao_Paulo"
        self.cache = {}
        self.last_update = None

    def _get_forecast_data(self) -> Optional[Dict]:
        """Busca dados da API com cache de 10 minutos"""
        if self.last_update and (datetime.now() - self.last_update) < timedelta(minutes=10):
            return self.cache
        
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "temperature_2m,weathercode,precipitation_probability",
            "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum",
            "timezone": self.timezone,
            "forecast_days": 7,
            "current_weather": True
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            self.cache = response.json()
            self.last_update = datetime.now()
            return self.cache
        except Exception as e:
            print(f"Erro ao acessar Open-Meteo: {e}")
            return None

    def _interpret_weathercode(self, code: int) -> str:
        weather_codes = {
            0: "Céu limpo",
            1: "Parcialmente nublado",
            2: "Nublado",
            3: "Muito nublado",
            45: "Nevoeiro",
            51: "Chuvisco",
            61: "Chuva",
            80: "Chuva forte",
            95: "Trovoada",
        }
        return weather_codes.get(code, "Condição desconhecida")

    def obter_previsao(self, params: Dict) -> Dict:
        """Versão melhorada para integração com seu sistema"""
        data = self._get_forecast_data()
        if not data:
            return {"erro": "Serviço de clima indisponível"}

        periodo = params.get("periodo", "hoje")
        info = params.get("informacao", "geral")

        # Mapeamento de períodos
        days_map = {
            "hoje": 0,
            "amanha": 1,
            "depois de amanha": 2,
            "semana": 6,
            "fim de semana": self._get_weekend_index()
        }
        day_index = days_map.get(periodo, 0)

        try:
            # Dados atuais (se for hoje)
            current = data.get("current_weather", {})
            
            # Dados diários
            daily = data["daily"]
            date = daily["time"][day_index]
            
            response = {
                "cidade": "Porto Alegre",
                "data": date,
                "periodo": periodo,
                "condicao": self._interpret_weathercode(daily["weathercode"][day_index]),
                "temperatura_atual": f"{current.get('temperature', 'N/A')}°C" if day_index == 0 else None,
                "maxima": f"{daily['temperature_2m_max'][day_index]}°C",
                "minima": f"{daily['temperature_2m_min'][day_index]}°C",
                "precipitacao": f"{daily['precipitation_sum'][day_index]}mm",
                "probabilidade_chuva": f"{max(data['hourly']['precipitation_probability'][day_index*24:(day_index+1)*24])}%"
            }

            # Filtra resposta conforme o parâmetro solicitado
            if info == "temperatura":
                return {"resposta": f"Temperatura: {response['maxima']} (máx) / {response['minima']} (mín)"}
            elif info == "chuva":
                return {"resposta": f"Probabilidade de chuva: {response['probabilidade_chuva']}"}
            elif info == "sol":
                is_sunny = daily["weathercode"][day_index] in [0, 1]
                return {"resposta": "Haverá sol" if is_sunny else "Não haverá sol"}
            else:
                return response

        except Exception as e:
            return {"erro": f"Erro ao processar dados: {str(e)}"}

    def _get_weekend_index(self) -> int:
        today = datetime.now().weekday()
        return 5 - today if today < 5 else 0