from bark import generate_audio
import os
from scipy.io.wavfile import write as write_wav

# Create directory for audio if it doesn't exist
os.makedirs("app/audio", exist_ok=True)

text = "Hello, I'm the Daylily avatar speaking to you in real-time but i think its working"
print(f"Generating audio for text: '{text}'")

audio_array = generate_audio(text)
write_wav("app/audio/output_bark.wav", rate=24000, data=audio_array)
print("Audio saved to app/audio/output_bark.wav")