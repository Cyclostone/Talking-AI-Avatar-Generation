import os
import time
import sys
sys.path.append('app')
import run_pipeline as pipeline

def test_api_audio():
    """Test the API pipeline audio generation directly"""
    
    # Create unique test text with timestamp
    timestamp = time.strftime("%H:%M:%S")
    test_text = f"API PIPELINE TEST at {timestamp}: This should update the output_tts.wav file."
    
    print(f"🧪 Testing API pipeline audio generation")
    print(f"📝 Text: '{test_text}'")
    
    # Check current output_tts.wav file
    output_file = "app/audio/output_tts.wav"
    if os.path.exists(output_file):
        old_timestamp = os.path.getmtime(output_file)
        old_size = os.path.getsize(output_file)
        print(f"📁 Current output_tts.wav: {time.ctime(old_timestamp)} ({old_size} bytes)")
    else:
        print(f"📁 No existing output_tts.wav file")
    
    print(f"\n🎵 Calling pipeline.generate_voice()...")
    
    try:
        # Call the pipeline function directly
        audio_path = pipeline.generate_voice(test_text)
        print(f"✅ Pipeline returned: {audio_path}")
        
        # Check if file was updated
        if os.path.exists(output_file):
            new_timestamp = os.path.getmtime(output_file)
            new_size = os.path.getsize(output_file)
            print(f"📁 Updated output_tts.wav: {time.ctime(new_timestamp)} ({new_size} bytes)")
            
            if os.path.exists(output_file) and new_timestamp > old_timestamp:
                print(f"✅ SUCCESS: Audio file was updated!")
                return True
            else:
                print(f"❌ FAILURE: Audio file was NOT updated!")
                return False
        else:
            print(f"❌ FAILURE: Audio file does not exist!")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_api_audio()
