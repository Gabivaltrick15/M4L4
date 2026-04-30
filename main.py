import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import numpy as np

# Configurações iniciais
palavras = {
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}
translator = Translator()
recognizer = sr.Recognizer()

# 1. Escolhe uma palavra aleatória
palavra_pt = random.choice(palavras["médio"] + palavras["difícil"])

# 2. Traduz para o inglês (referência)
traducao_en = translator.translate(palavra_pt, src="pt", dest="en").text.lower()

print(f"Como se diz '{palavra_pt}' em inglês?")

# 3. Grava o áudio
fs = 16000
duracao = 3
print("Gravando...")
audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
sd.wait()
# Correção: conversão para int16 necessária para o arquivo wav ser legível
wav.write("output.wav", fs, (audio * 32767).astype('int16'))

# 4. Reconhece a voz
with sr.AudioFile("output.wav") as source:
    audio_data = recognizer.record(source)
    try:
        resposta = recognizer.recognize_google(audio_data, language="en-US").lower()
        print(f"Você disse: {resposta}")

        # 5. Compara (deve estar dentro do try, pois depende da variável 'resposta')
        if resposta == traducao_en:
            print("Acertou!")
        else:
            print(f"Errou! O correto era: {traducao_en}")

    except sr.UnknownValueError:
        print("Não consegui entender o áudio.")
        
    except sr.RequestError:
        print("Erro de conexão com o serviço de reconhecimento.")
