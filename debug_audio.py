import os
import time
from gtts import gTTS
from pydub import AudioSegment

# Test text with timestamp
timestamp = time.strftime("%H:%M:%S")
test_text = f"DEBUG TEST at {timestamp}: This should create a new audio file."

print(f"🧪 Testing gTTS directly with text: '{test_text}'")
print(f"Current working directory: {os.getcwd()}")

# Create output directory
audio_dir = "app/audio"
os.makedirs(audio_dir, exist_ok=True)
print(f"📁 Audio directory: {os.path.abspath(audio_dir)}")

# Test gTTS directly
try:
    print("🎵 Creating gTTS object...")
    tts = gTTS(text=test_text, lang='en', slow=False)
    
    # Save as MP3 first
    mp3_path = f"{audio_dir}/debug_test.mp3"
    print(f"💾 Saving MP3 to: {os.path.abspath(mp3_path)}")
    tts.save(mp3_path)
    
    if os.path.exists(mp3_path):
        mp3_size = os.path.getsize(mp3_path)
        print(f"✅ MP3 created successfully! Size: {mp3_size} bytes")
        
        # Convert to WAV
        wav_path = f"{audio_dir}/debug_test.wav"
        print(f"🔄 Converting to WAV: {os.path.abspath(wav_path)}")
        
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        
        if os.path.exists(wav_path):
            wav_size = os.path.getsize(wav_path)
            print(f"✅ WAV created successfully! Size: {wav_size} bytes")
            
            # Clean up MP3
            os.remove(mp3_path)
            print(f"🗑️ Cleaned up MP3 file")
            
            # List all files in audio directory
            print(f"\n📂 Files in audio directory:")
            for file in os.listdir(audio_dir):
                file_path = os.path.join(audio_dir, file)
                file_size = os.path.getsize(file_path)
                file_time = time.ctime(os.path.getmtime(file_path))
                print(f"  - {file} ({file_size} bytes, {file_time})")
                
        else:
            print(f"❌ WAV conversion failed!")
    else:
        print(f"❌ MP3 creation failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
