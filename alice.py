#!/usr/bin/python3

# Nome - Alice
# Nome de Fabrica - 4L1C3-1107
# Inicio - 11/07/2020

import sys


import os, platform, datetime, pywhatkit
# Voz
import speech_recognition as sr # Reconhecer voz
from gtts import gTTS # Criar os arquivos de audio
from playsound import playsound # Tocar os arquivos de audio
# Chatbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer # import metodo de treino

"""

"""


# Fala
r = sr.Recognizer()


# Cores
class tcolors:
    BLACK = '\033[1;30m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    LPURPLE = '\033[1;35m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Chatbot
class AliceIA():

    reco = sr.Recognizer() 

    chatbot = ChatBot( # Cria o bot
        'Alice'
        # preprocessors=['chatterbot.preprocessors.clean_whitespace'],
        # read_only=True # Faz com que o bot pare de aprender
    )

    confi_list = ["Não entendi oque você falou"]
    trainer = ChatterBotCorpusTrainer(chatbot) # diferente do ListTrainer, esse trainer le yml e json
    trainer.train('falas/')

    def message(message):
        print(tcolors.ENDC + tcolors.GREEN + 'Alice:' + tcolors.BOLD + tcolors.YELLOW, message)

    def runBot():
        clear()
        # Run bot
        while True:
            
            try:
                with sr.Microphone() as botSource:  # Usando o microfone
                    AliceIA.reco.adjust_for_ambient_noise(botSource) # Chama um algoritmo de redução de ruidos no som

                    print(tcolors.BLUE + "\nVocê: ", end="")

                    voice = AliceIA.reco.listen(botSource) # Armazena o que foi dito numa variavel (escuta)
                    req = AliceIA.reco.recognize_google(voice,language='pt-BR') #Entende

                    print(tcolors.BOLD + tcolors.YELLOW, end="") # Ordenar cores
                    request = req # request = entende
                    print(request)
                    response = AliceIA.chatbot.get_response(request)

                    if request.lower() in ["sair", "tchau", "saiu"]:
                        AliceIA.message("Mas já?")
                        speak("Mas já?", show=False)
                        print(tcolors.ENDC)
                        break
                    else:
                        response = str(response)
                        AliceIA.message(response)
                        speak(response, show=False)
            except Exception:
                pass

# Função para limpar o terminal
def clear(): 
	if platform.system() == 'Linux':
		os.system('clear')
	else:
		os.system('cls')

def speak(text, show=True):
    language = 'pt-br'

    if show:
        print(text.strip())

    aliceVoice = gTTS(text=text, lang=language, slow=False)
    aliceVoice.save("speak.mp3") # Salva
    playsound("speak.mp3") # Reproduz
    os.remove("speak.mp3") # Apaga

clear() # limpa o terminal

            # == DEV == 
# speak("Olá, eu sou a Alice")
# speak("Como eu posso ser útil?")


def take_command():
    try:
        with sr.Microphone() as source:  # Usando o microfone

            r.adjust_for_ambient_noise(source) # Chama um algoritmo de redução de ruidos no som
            clear()

            print(tcolors.YELLOW + "Escutando... " + tcolors.ENDC) # Frase para o usuario dizer algo

            # voice = r.listen(source) # Armazena o que foi dito numa variavel (escuta)
            # command = r.recognize_google(voice,language='pt-BR') # Passa a variável para o algoritmo reconhecedor de padroes

            command = input("Dev: ")
            command = command.lower()

            if  command.startswith("alice") or command.endswith("alice"):
                command = command.replace("alice", "")
                print("Voce disse:" + command)
                return command

    except Exception:
        pass

def run_alice():  # sourcery skip: remove-pass-

    command = take_command()

    # try:
    if "tocar" in command:
        song = command.replace("tocar", "")
        speak("Tocando", song)
        pywhatkit.playonyt(song)

    elif "horas" in command:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("São " + time)

    elif "pesquisar" in command or "pesquise" in command or "procurar" in command:
        search = command.replace("pesquisar", "").replace("procurar", "").replace("por", "")

        speak("Ok, pesquisando por", search)
        pywhatkit.search(search)

    elif "repita" in command or "fale" in command or "diga" in command:
        talk = command.replace("repita", "").replace("fale", "")
        speak(talk)

    elif command in ["oi", "bom dia"]:
        speak("Olá como você está?")

    elif "sair" in command or "tchau" in command or "adeus" in command:
        speak("Foi um prazer")
        exit()

    elif "chat" in command or "conversar" in command:
        speak("Vamos conversar")
        AliceIA.runBot()

    else:
        speak("Okay")
        pywhatkit.search(command)

    # except Exception:
    #     pass

while True:
    run_alice()
