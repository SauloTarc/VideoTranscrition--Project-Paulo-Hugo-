from moviepy.editor import VideoFileClip
import speech_recognition as sr
import yt_dlp

def baixar_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Ou use 'mp3' se preferir esse formato
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s'  # Salva o áudio com o nome 'audio.wav'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcrever_audio(caminho_audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(caminho_audio) as source:
        audio = recognizer.record(source)
    
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("Transcrição:", texto)
    except sr.RequestError as e:
        print(f"Erro de requisição: {e}")
    except sr.UnknownValueError:
        print("Google Speech Recognition não conseguiu entender o áudio")
        with open("transcricao.txt", "w") as file:
            file.write(texto)

def processar_video_youtube(url):
    baixar_audio(url)
    transcrever_audio('audio.wav')