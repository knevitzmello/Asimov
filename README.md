# Assistente Virtual Asimov

Este projeto implementa um assistente virtual personalizado integrado ao Home Assistant (HASS). O assistente responde à palavra de ativação "Asimov", detectada através de um modelo treinado no Vosk.

## Funcionalidades

- Ativação por voz: Utiliza um modelo do Vosk para reconhecer a palavra "Asimov".

- Controle de dispositivos: Permite interagir com luzes, música e outros dispositivos via API.

- Integração com Home Assistant: Projetado para funcionar com o HASS, mas pode ser expandido para outras plataformas.

- Expansível: Pode ser ajustado para incluir novos comandos e interações personalizadas.

## Tecnologias Utilizadas

- Vosk - Reconhecimento de fala offline.

- Home Assistant - Automação residencial.

- APIs REST - Comunicação com dispositivos e serviços.

## Instalação

1 - Clone este repositório:

``
git clone https://github.com/seu-usuario/seu-repositorio.git](https://github.com/knevitzmello/Asimov.git
``

``
cd seu-repositorio
``

2 - Crie um ambiente virtual e instale as dependências (em construção):

``
pip install -r requirements.txt
``

3 - Configure as credenciais e endpoints no arquivo de configuração.


4 - Crie as Automations no HASS que, ao receber o webhook, realizam uma ação (ver arquivo .yaml)

# Uso

Execute o assistente:

``
python main.py
``

Diga "Asimov" para ativar o assistente e emita comandos de voz.

Expanda as funcionalidades editando os arquivos de configuração e as integrações com APIs.
