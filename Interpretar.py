from os import replace
import re
from datetime import datetime, timedelta

class Interpretar:
    def __init__(self):
        """Define palavras-chave para classificar comandos rapidamente"""
        self.verbos = {
            "reproduzir_musica": {"tocar", "reproduzir", "toca", "reproduza", "reproduz"},
            "pausar_musica": {"pausar", "parar", "pare", "pause"},
            "continuar_musica": {"continuar"},
            "ajustar_volume": {"volume", "diminuir", "aumentar", "ajuste", "diminua", "aumente"},
            "set_alarm": {"alarme", "despertar", "despertador"},
            "set_despertador": {"acordar"},
            "set_horadedormir": {"dormir"},
            "turn_on_light": {"ligar", "acender", "ligue", "acenda", "liga", "acende", "ajuste", "ajustar"},
            "turn_off_light": {"desligar", "apagar", "desligue", "apague", "apaga", "desliga", "desative", "desativar", "ativar", "ative"},
            "lista": {"adicionar", "adicione", "inclua", "comprar","insira", "acrescentar", "incluir", "inserir", "põe", "lista", "compras"},
            "set_timer": {"timer", "avise", "avisar", "lembre-me", "lembrar"}
        }
        self.areas_validas = {"sala", 
                              "quarto", 
                              "escritório", 
                              "cozinha", 
                              "luminárias", 
                              "luminarias", 
                              "Bancada",
                              "Bancada 1", 
                              "Bancada 2", 
                              "Bancada 3"}
        self.verbos_compras = {"coloque", "coloca"}
    
    def classificar_intencao(self, frase):
        frase = frase.lower()
        
        if re.search(r"alarme\s+em", frase):
            return "set_timer"
        
        if "alarme" in frase:
            return "set_alarm"
        
        palavras = set(frase.split())
        for intent, verbos in self.verbos.items():
            if palavras & verbos:
                return intent
        
        return "unknown"

    def extrair_parametros(self, frase, intent):
        extratores = {
            "reproduzir_musica": self._extrair_musica,
            "ajustar_volume": self._extrair_volume,
            "set_alarm": self._extrair_alarme,
            "set_despertador": self._extrair_alarme,
            "set_horadedormir": self._extrair_alarme,
            "turn_on_light": self._extrair_luz,
            "turn_off_light": self._extrair_luz,
            "lista": self._extrair_lista
        }
        
        if intent in extratores:
            return extratores[intent](frase, intent)
        
        return {}

    def _extrair_musica(self, frase, intent):
        parametros = {}
        verbos_musica = self.verbos["reproduzir_musica"]
        verbos_reproduzir_musica = "|".join(re.escape(verbo) for verbo in verbos_musica)

        match = re.search(
            rf"^\s*(?:{verbos_reproduzir_musica})\s+(?P<musica>.+?)(?:\s+no\s+(?P<fonte>Spotify|YouTube))?$",
            frase,
            re.IGNORECASE
        )
        if match:
            parametros["musica"] = match.group("musica").strip()
            parametros["fonte"] = match.group("fonte").strip() if match.group("fonte") else "Spotify"
        return parametros

    def _extrair_volume(self, frase, intent):
        match = re.search(r"\b(100|[1-9]?[0-9])\b", frase, re.IGNORECASE)
        return {"volume": int(match.group(0))} if match else {}

    def _extrair_alarme(self, frase, intent):
        parametros = {}
        match = re.search(
            r'(?:daqui|em|dentro de|faltam|faltando|após|depois de)\s+(\d{1,2})\s*(horas?|h)?(?:\s*(?:e)?\s*(\d{1,2})\s*(minutos?|m)?)?',
            frase, re.IGNORECASE
        )
        if match:
            horas = int(match.group(1)) if match.group(2) else 0
            minutos = int(match.group(3)) if match.group(4) else (int(match.group(1)) if not match.group(2) else 0)

            agora = datetime.now()
            hora_alvo = agora + timedelta(hours=horas, minutes=minutos)
            parametros["horario"] = hora_alvo.strftime("%H:%M")
            return parametros

        padroes_abs = [
            r'(\d{1,2}:\d{2})',
            r'(\d{1,2}h\d{2})',
            r'(\d{1,2} horas?)',
            r'(\d{1,2}h)',
            r'\bàs (\d{1,2})\b',
            r'\b(\d{1,2})\b'
        ]

        for padrao in padroes_abs:
            match = re.search(padrao, frase, re.IGNORECASE)
            if match:
                hora_raw = match.group(1)
                hora_formatada = self._normalizar_horario(hora_raw)
                if hora_formatada:
                    parametros["horario"] = hora_formatada
                    return parametros

        return parametros

    def _normalizar_horario(self, texto):
        texto = texto.strip().lower()

        if re.match(r'^\d{1,2}:\d{2}$', texto):
            return texto
        if re.match(r'^\d{1,2}h\d{2}$', texto):
            partes = texto.split('h')
            return f'{int(partes[0])}:{int(partes[1]):02d}'
        if re.match(r'^\d{1,2}h$', texto) or re.match(r'^\d{1,2} horas?$', texto):
            hora = re.findall(r'\d{1,2}', texto)[0]
            return f'{int(hora)}:00'
        if re.match(r'^\d{1,2}$', texto):
            return f'{int(texto)}:00'

        return None


    def _normalizar_horario(self, texto):
        texto = texto.strip().lower()

        # Se já estiver no formato HH:MM
        if re.match(r'^\d{1,2}:\d{2}$', texto):
            return texto

        # Formato HHhMM (ex: 7h30)
        if re.match(r'^\d{1,2}h\d{2}$', texto):
            partes = texto.split('h')
            return f'{int(partes[0])}:{int(partes[1]):02d}'

        # Formato HHh ou "HH horas"
        if re.match(r'^\d{1,2}h$', texto) or re.match(r'^\d{1,2} horas?$', texto):
            hora = re.findall(r'\d{1,2}', texto)[0]
            return f'{int(hora)}:00'

        # Apenas número (ex: "às 7")
        if re.match(r'^\d{1,2}$', texto):
            return f'{int(texto)}:00'

        return None

    def _extrair_luz(self, frase, intent):
        parametros = {"intensidade": 0 if intent == "turn_off_light" else 100}
        match_area = re.search(r"(?:no|na|do|da)?\s?(?P<area>" + "|".join(self.areas_validas) + r")(\W|$)", frase, re.IGNORECASE)
        match_percentual = re.search(r"(?:em|para)?\s?(?P<intensidade>\d{1,3})\%?", frase, re.IGNORECASE)
        
        if match_area:
            parametros["area"] = match_area.group("area") if match_area.group("area") else "todas"
        if match_percentual:
            intensidade = int(match_percentual.group("intensidade"))
            if 0 <= intensidade <= 100:
                parametros["intensidade"] = intensidade
        if parametros["area"] == "sala":
            parametros["area"] = "sala_de_estar"
        
        return parametros

    def _extrair_lista(self, frase, intent):
        parametros = {"lista": "compras"}  # Padrão
        verbos_lista_de_compras = self.verbos["lista"] | self.verbos_compras
        verbos_lista = "|".join(re.escape(verbo) for verbo in verbos_lista_de_compras)
        
        regex_item = rf"(?:{verbos_lista})\s+(?P<item>.+?)(?:\s+(?:na|à|a)?\s*lista de (?P<tipo_lista>\w+))?$"
        match = re.search(regex_item, frase, re.IGNORECASE)
        
        if match:
            parametros["item"] = match.group("item").strip()
            if match.group("tipo_lista"):
                parametros["lista"] = match.group("tipo_lista").strip()
        
        return parametros

    def process_message(self, frase):
        """Recebe a frase, classifica o comando e extrai parâmetros"""
        intent = self.classificar_intencao(frase)
        parametros = self.extrair_parametros(frase, intent) if intent != "unknown" else {}
        return intent, parametros


