import os
import subprocess
import sys

# Install dependencies first
print("Installing gTTS and pydub...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts", "pydub"])
    print("✅ Dependencies installed successfully")
except Exception as e:
    print(f"❌ Failed to install dependencies: {e}")
    exit(1)

# Now test gTTS
from gtts import gTTS
from pydub import AudioSegment

# Create output directory
os.makedirs("app/audio", exist_ok=True)

# Test text - unique message
text = "TESTING GTTS: This is a unique test message to verify gTTS audio generation works correctly."
print(f"Generating audio for text: '{text}'")

try:
    # Generate audio using gTTS
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save as MP3 first
    temp_mp3 = "app/audio/test_gtts.mp3"
    tts.save(temp_mp3)
    print(f"✅ MP3 audio saved: {temp_mp3}")
    
    # Convert to WAV
    audio = AudioSegment.from_mp3(temp_mp3)
    wav_path = "app/audio/test_gtts.wav"
    audio.export(wav_path, format="wav")
    print(f"✅ WAV audio saved: {wav_path}")
    
    # Clean up temp file
    os.remove(temp_mp3)
    
    print("🎉 gTTS test completed successfully!")
    
except Exception as e:
    print(f"❌ gTTS test failed: {e}")
    exit(1)
