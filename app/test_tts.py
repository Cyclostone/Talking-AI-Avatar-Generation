import os
from TTS.api import TTS

# Create output directory
os.makedirs("app/audio", exist_ok=True)

# Text to convert to speech - UNIQUE TEST TEXT
text = "This is a unique test message to verify text generation works correctly."
print(f"Generating audio for text: '{text}'")

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# Generate audio
output_path = "app/audio/test_direct.wav"
tts.tts_to_file(text=text, file_path=output_path)

print(f"Audio saved to {output_path}")
