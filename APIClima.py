import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

class APIClima():
    def __init__(self, api_key: str):
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.api_key = api_key
        self.cidade = "Porto Alegre,BR"
        
        # Mapeamento de períodos para dias
        self.periodo_para_dias = {
            "hoje": 0,
            "amanha": 1,
            "depois de amanha": 2,
            "semana": 7,
            "fim de semana": self._dias_para_fim_de_semana()
        }
        
        # Mapeamento de tipos de informação para campos da API
        self.info_para_campo = {
            "temperatura": "temp",
            "maxima": "temp_max",
            "minima": "temp_min",
            "chuva": "rain",
            "sol": "clear",
            "umidade": "humidity",
            "vento": "wind_speed",
            "geral": "all"
        }

    def _dias_para_fim_de_semana(self) -> int:
        """Calcula quantos dias faltam para o próximo fim de semana"""
        hoje = datetime.now().weekday()  # 0=segunda, 6=domingo
        if hoje >= 5:  # Já é fim de semana
            return 0
        return 5 - hoje  # Sexta-feira

    def _converter_kelvin_para_celsius(self, temp_k: float) -> float:
        """Converte temperatura de Kelvin para Celsius"""
        return temp_k - 273.15

    def _obter_previsao(self) -> Optional[Dict]:
        """Obtém os dados brutos da API"""
        try:
            params = {
                'q': self.cidade,
                'appid': self.api_key,
                'lang': 'pt_br'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar API de clima: {e}")
            return None

    def _processar_dados(self, dados: Dict, periodo: str, info: str) -> Dict:
        """Processa os dados brutos da API conforme os parâmetros solicitados"""
        if not dados or 'list' not in dados:
            return {"erro": "Dados de clima não disponíveis"}

        dias = self.periodo_para_dias.get(periodo, 0)
        data_alvo = (datetime.now() + timedelta(days=dias)).date()
        
        # Filtra previsões para o período solicitado
        previsoes_periodo = [
            p for p in dados['list'] 
            if datetime.fromtimestamp(p['dt']).date() == data_alvo
        ]
        
        if not previsoes_periodo:
            return {"erro": f"Previsão não disponível para {periodo}"}

        # Processa conforme o tipo de informação solicitada
        resultado = {}
        campo = self.info_para_campo.get(info, "all")
        
        if campo == "temp":
            temps = [self._converter_kelvin_para_celsius(p['main']['temp']) for p in previsoes_periodo]
            resultado["temperatura"] = f"{round(sum(temps)/len(temps), 1)}°C"
        
        elif campo == "temp_max":
            max_temp = max(p['main']['temp_max'] for p in previsoes_periodo)
            resultado["temperatura_maxima"] = f"{round(self._converter_kelvin_para_celsius(max_temp), 1)}°C"
        
        elif campo == "temp_min":
            min_temp = min(p['main']['temp_min'] for p in previsoes_periodo)
            resultado["temperatura_minima"] = f"{round(self._converter_kelvin_para_celsius(min_temp), 1)}°C"
        
        elif campo == "humidity":
            umidades = [p['main']['humidity'] for p in previsoes_periodo]
            resultado["umidade"] = f"{round(sum(umidades)/len(umidades), 1)}%"
        
        elif campo == "wind_speed":
            ventos = [p['wind']['speed'] for p in previsoes_periodo]
            resultado["vento"] = f"{round(sum(ventos)/len(ventos), 1)} km/h"
        
        elif campo == "rain":
            chuva = any('rain' in p for p in previsoes_periodo)
            resultado["chuva"] = "Sim" if chuva else "Não"
        
        elif campo == "clear":
            sol = any(p['weather'][0]['main'].lower() in ['clear', 'sun'] for p in previsoes_periodo)
            resultado["sol"] = "Sim" if sol else "Não"
        
        else:  # Geral
            temps = [self._converter_kelvin_para_celsius(p['main']['temp']) for p in previsoes_periodo]
            descricao = previsoes_periodo[0]['weather'][0]['description']
            
            resultado.update({
                "descricao": descricao.capitalize(),
                "temperatura": f"{round(sum(temps)/len(temps), 1)}°C",
                "umidade": f"{previsoes_periodo[0]['main']['humidity']}%",
                "vento": f"{previsoes_periodo[0]['wind']['speed']} km/h"
            })
        
        resultado["periodo"] = periodo
        resultado["data"] = data_alvo.strftime("%d/%m/%Y")
        resultado["cidade"] = self.cidade.split(',')[0]
        
        return resultado

    def obter_previsao(self, parametros: Dict) -> Dict:
        """
        Obtém a previsão do tempo com base nos parâmetros extraídos
        
        Args:
            parametros: Dicionário com 'informacao' e 'periodo' (ex: {'informacao': 'temperatura', 'periodo': 'amanha'})
        
        Returns:
            Dicionário com os dados de previsão formatados
        """
        info = parametros.get("informacao", "geral")
        periodo = parametros.get("periodo", "hoje")
        
        dados = self._obter_previsao()
        if not dados:
            return {"erro": "Não foi possível obter dados do clima"}
        
        return self._processar_dados(dados, periodo, info)