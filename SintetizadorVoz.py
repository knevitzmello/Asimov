import pyttsx3
import re

class SintetizadorVoz:
    def __init__(self):
        """Inicializa o sintetizador de voz com configurações padrão"""
        self._motor = pyttsx3.init()
        self._caracteres_ignorar = {'°', 'º', 'ª', '*', '[', ']'}  # Caracteres a serem removidos
        self._configurar_padroes()
    
    def _configurar_padroes(self):
        """Configura os parâmetros padrão da voz"""
        vozes = self._motor.getProperty('voices')
        
        # Tenta encontrar uma voz feminina em português
        for voz in vozes:
            if 'pt-br' in str(voz.languages).lower() and 'female' in voz.id.lower():
                self._motor.setProperty('voice', voz.id)
                break
        else:
            self._motor.setProperty('voice', vozes[0].id)
        
        self._motor.setProperty('rate', 210)
        self._motor.setProperty('volume', 0.9)
        self._motor.setProperty('edge', 'soft')
    
    def _filtrar_texto(self, texto):
        """Remove caracteres indesejados e formata para fala natural"""
        # Remove caracteres especiais
        for char in self._caracteres_ignorar:
            texto = texto.replace(char, '')
        
        # Simplifica datas (transforma "15/03/2024" em "15 de março")
        texto = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', self._formatar_data, texto)
        
        return texto.strip()
    
    def _formatar_data(self, match):
        """Formata a data para formato falado"""
        dia = match.group(1)
        mes = self._numero_para_mes(int(match.group(2)))
        return f"{dia} de {mes}"
    
    def _numero_para_mes(self, numero_mes):
        """Converte número do mês para nome"""
        meses = [
            'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
        ]
        return meses[numero_mes - 1] if 1 <= numero_mes <= 12 else f'mês {numero_mes}'
    
    def falar(self, texto):
        """
        Sintetiza e reproduz o texto fornecido após filtragem
        Args:
            texto (str): Texto a ser falado
        """
        try:
            texto_filtrado = self._filtrar_texto(texto)
            self._motor.say(texto_filtrado)
            self._motor.runAndWait()
        except Exception as e:
            print(f"Erro na síntese de voz: {e}")
    
    def adicionar_caracteres_ignorar(self, caracteres):
        """Adiciona caracteres à lista de ignorados"""
        self._caracteres_ignorar.update(caracteres)
    
    def __del__(self):
        """Libera recursos do sintetizador"""
        self._motor.stop()