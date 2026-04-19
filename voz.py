import wave 
from piper import PiperVoice
from playsound3 import playsound

voice = PiperVoice.load(r"C:\Voz_Nous\Vozes\pt_BR-faber-medium.onnx")

def criar_audio(Nous):
    
    with wave.open("Nous_output.wav", "wb") as wav_file:
        voice.synthesize_wav(Nous, wav_file)
    playsound("Nous_output.wav", block=True)