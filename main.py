# Imports necesarios
import tkinter as tk
from tkinter import messagebox
import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# Diccionario de palabras por nivel
words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["platano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

# Traducciones al inglés
translations = {
    "gato": "cat", "perro": "dog", "manzana": "apple", "leche": "milk", "sol": "sun",
    "platano": "banana", "escuela": "school", "amigo": "friend", "ventana": "window", "amarillo": "yellow",
    "tecnologia": "technology", "universidad": "university", "informacion": "information",
    "pronunciacion": "pronunciation", "imaginacion": "imagination"
}

# Funciones de voz
def grabar_audio(nombre_archivo="voz.wav", duracion=4, fs=44100):
    print("Habla ahora...")
    audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(nombre_archivo, fs, audio)
    return nombre_archivo

def reconocer_audio(nombre_archivo="voz.wav"):
    r = sr.Recognizer()
    with sr.AudioFile(nombre_archivo) as source:
        audio = r.record(source)
    try:
        texto = r.recognize_google(audio, language="en-US")
        return texto.lower()
    except:
        return ""

# Interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Habla Correcto")
ventana.geometry("450x300")

# Variables de juego
nivel = "facil"
puntos = 0
errores = 0
palabra_actual = tk.StringVar()

def seleccionar_nivel(n):
    global nivel, puntos, errores
    nivel = n
    puntos = 0
    errores = 0
    etiqueta_puntos.config(text="Puntos: 0 | Errores: 0/3")
    nueva_palabra()

def nueva_palabra():
    global palabra_actual
    palabra_actual.set(random.choice(words_by_level[nivel]))
    etiqueta_palabra.config(text=f"Traduce: {palabra_actual.get()}")

def verificar():
    global puntos, errores
    archivo = grabar_audio()
    respuesta = reconocer_audio(archivo)
    correcta = translations[palabra_actual.get()]
    if respuesta == correcta:
        puntos += 1
        etiqueta_resultado.config(text="Correcto")
    else:
        errores += 1
        etiqueta_resultado.config(text=f"Incorrecto. Era: {correcta}")
    etiqueta_puntos.config(text=f"Puntos: {puntos} | Errores: {errores}/3")
    if errores >= 3:
        messagebox.showinfo("Fin del juego", f"Puntuación final: {puntos}")
        ventana.quit()
    else:
        nueva_palabra()

# Widgets
etiqueta_palabra = tk.Label(ventana, text="Selecciona un nivel para comenzar", font=("Arial", 14))
etiqueta_palabra.pack(pady=10)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

btn_facil = tk.Button(frame_botones, text="Fácil", command=lambda: seleccionar_nivel("facil"), bg="#4CAF50", fg="white")
btn_facil.grid(row=0, column=0, padx=5)

btn_medio = tk.Button(frame_botones, text="Medio", command=lambda: seleccionar_nivel("medio"), bg="#FFC107", fg="black")
btn_medio.grid(row=0, column=1, padx=5)

btn_dificil = tk.Button(frame_botones, text="Difícil", command=lambda: seleccionar_nivel("dificil"), bg="#F44336", fg="white")
btn_dificil.grid(row=0, column=2, padx=5)

boton_verificar = tk.Button(ventana, text="Verificar pronunciación", command=verificar, bg="#2196F3", fg="white")
boton_verificar.pack(pady=10)

etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 12, "bold"))
etiqueta_resultado.pack(pady=10)

etiqueta_puntos = tk.Label(ventana, text="Puntos: 0 | Errores: 0/3", font=("Arial", 12))
etiqueta_puntos.pack(pady=5)

ventana.mainloop()
