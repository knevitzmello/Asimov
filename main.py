﻿import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import os
import json
import requests
from AlarmAPI import AlarmAPI
from Interpretar import Interpretar
from ControlarLuzAPI import ControlarLuzAPI
from SpotifyAPI import SpotifyAPI
from GrocyAPI import GrocyAPI
import pyttsx3
import SystemVolume as sv
import threading

def carregar_secrets():
    with open("secrets.json", "r") as file:
        return json.load(file)

secrets = carregar_secrets()

porcupine_access_key = secrets["pvporcupine_access_key"]
spotify = SpotifyAPI(
    client_id=secrets["spotify"]["client_id"],
    client_secret=secrets["spotify"]["client_secret"],
    redirect_uri=secrets["spotify"]["redirect_uri"],
    device_id= "DESKTOP-F9SQIII"
)


home_assistant_webhook_url_controlar_luz = secrets["home_assistant"]["controlar_luz"]
home_assistant_webhook_url_grocy= secrets["home_assistant"]["grocy"]
home_assistant_webhook_url_alarm = secrets["home_assistant"]["alarm"]

caminho_modelos = os.path.join(os.path.dirname(__file__), "modelos")
caminho_wakeword_asimov = os.path.join(caminho_modelos, "Asimov_en_windows_v3_0_0.ppn")

porcupine = pvporcupine.create(
    access_key=porcupine_access_key,
    keyword_paths=[caminho_wakeword_asimov]
)

grocy = GrocyAPI(
    base_url=secrets["grocy"]["base_url"],
    api_key=secrets["grocy"]["api_key"],
    home_assistant_webhook_url_grocy = home_assistant_webhook_url_grocy,
)
recognizer = sr.Recognizer()
microfone = sr.Microphone()
alarmAPI = AlarmAPI(home_assistant_webhook_url_alarm)
controlarLuz = ControlarLuzAPI(home_assistant_webhook_url_controlar_luz)
interpretar = Interpretar()
paud = pyaudio.PyAudio()
vol = sv.SystemVolume()

speaker=pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[0].id)
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate+10)

def speak(text):
    speaker.say(text)
    speaker.runAndWait()
    speaker.stop()

def selecionar_dispositivo_audio():
    print("Dispositivos de entrada de áudio disponíveis:")
    for i in range(paud.get_device_count()):
        info = paud.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"{i}: {info['name']}")
    return int(input("Digite o índice do dispositivo desejado: "))

#indice_dispositivo = selecionar_dispositivo_audio()

indice_dispositivo = 1

audio_stream = paud.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
    input_device_index=indice_dispositivo
)

def executar_comando(comando, parametros):

    if any(value is None for value in parametros.values()):
        print("Não entendi o comando")
        #threading.Thread(target=speak, args=("Não entendi o comando",)).start()
    else:
        match comando:
            case "criar_alarme":
                alarmAPI.criar_alarme(parametros)
            case "turn_on_light":
                controlarLuz.enviar_webhook("on", parametros.get('area'))
            case "turn_off_light":
                controlarLuz.enviar_webhook("off", parametros.get('area'))
            case "reproduzir_musica":
                if parametros:
                    musica = parametros.get('musica', None)
                if musica != None:
                    spotify.play_music(musica)
            case "set_despertador":
                alarmAPI.criar_despertador(parametros.get('horario', None))
            case "set_horadedormir":
                alarmAPI.set_horadedormir(parametros.get('horario', None))
            case "ajustar_volume":
                vol.set_volume_percent(parametros.get('volume'))
            case "pausar_musica":
                spotify.pause_playback()
            case "continuar_musica":
                spotify.resume_playback()
            case "lista":
                add_item(parametros)

def add_item(parametros):
    if parametros:
        lista = parametros.get('lista')
        item = parametros.get('item')
        if lista == 'compras':
            print("Resposta:", grocy.add_shopping_list_item(item))
        elif lista == 'tarefas':
            print("Resposta:", grocy.add_task(item))

def interpreta_comando(texto_detectado):
    comando, parametros = interpretar.process_message(texto_detectado)
    executar_comando(comando, parametros)

def transcrever_audio():
    with microfone as source:
        #recognizer.adjust_for_ambient_noise(source)
        print("Ouvindo para transcrição...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            try:
                transcricao = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Comando detectado: {transcricao}")
                interpreta_comando(transcricao)
                vol.set_volume_percent(currentVolume)
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio")
            except sr.RequestError as e:
                print(f"Erro na requisição ao Google: {e}")
        except sr.WaitTimeoutError:
            print("Tempo esgotado. Nenhum áudio detectado.")
        except sr.UnknownValueError:
            print("Microfone não está disponível ou não funcionando corretamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

def ouvir_wakeword():
    print("Aguardando wakeword...")
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        if porcupine.process(pcm_unpacked) >= 0:
            print("Wakeword detectada!")
            currentVolume = vol.get_volume_percent()
            vol.set_volume_percent(5)
            transcrever_audio()
            vol.set_volume_percent(currentVolume)

currentVolume = vol.get_volume_percent()
ouvir_wakeword()

#vol.set_volume_percent(5)
#interpreta_comando("ligar casa")
#vol.set_volume_percent(currentVolume)