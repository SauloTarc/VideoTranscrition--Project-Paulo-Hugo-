from moviepy.editor import VideoFileClip
import speech_recognition as sr
import yt_dlp
from pydub import AudioSegment
import os

def baixar_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def dividir_audio(caminho_audio, duracao_segmento=150000):
    # Carregar o áudio
    audio = AudioSegment.from_wav(caminho_audio)
    tamanho_audio = len(audio)
    
    # Dividir o áudio em segmentos menores de duracao_segmento (milissegundos)
    segmentos = []
    for i in range(0, tamanho_audio, duracao_segmento):
        segmento = audio[i:i+duracao_segmento]
        # Salva o segmento temporariamente
        caminho_segmento = f"segmento_{i//duracao_segmento}.wav"
        segmento.export(caminho_segmento, format="wav")
        segmentos.append(caminho_segmento)
    
    return segmentos

def transcrever_audio_segmento(caminho_segmento, recognizer):
    with sr.AudioFile(caminho_segmento) as source:
        audio = recognizer.record(source)
    
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        return texto
    except sr.RequestError as e:
        print(f"Erro de requisição: {e}")
        return ""
    except sr.UnknownValueError:
        print("Google Speech Recognition não conseguiu entender o áudio")
        return ""

def transcrever_audio(caminho_audio):
    recognizer = sr.Recognizer()
    segmentos = dividir_audio(caminho_audio)
    
    transcricao_completa = ""
    for i, caminho_segmento in enumerate(segmentos):
        print(f"Transcrevendo segmento {i+1}/{len(segmentos)}...")
        transcricao_completa += transcrever_audio_segmento(caminho_segmento, recognizer) + " "
        # Remove o arquivo de segmento após a transcrição
        print(transcricao_completa)
        os.remove(caminho_segmento)

    with open("transcricao.txt", "w") as file:
        file.write(transcricao_completa)

def processar_video_youtube(url):
    baixar_audio(url)
    transcrever_audio('audio.wav')