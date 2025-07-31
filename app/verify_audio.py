import os
import subprocess
import time

def test_audio_generation():
    """Test audio generation with unique text"""
    
    # Create unique test text with timestamp
    timestamp = time.strftime("%H:%M:%S")
    test_text = f"AUDIO VERIFICATION TEST at {timestamp}. This is a unique message to verify audio generation is working correctly."
    
    print(f"🧪 Testing audio generation with text: '{test_text}'")
    
    # Generate audio using our gTTS script - use absolute path
    output_filename = f"verify_test_{timestamp.replace(':', '_')}.wav"
    output_path = f"app/audio/{output_filename}"
    abs_output_path = os.path.abspath(output_path)
    
    command = [
        "python", "generate_audio_gtts.py",
        "--text", test_text,
        "--output", output_path
    ]
    
    print(f"Running: {' '.join(command)}")
    print(f"Expected output: {abs_output_path}")
    
    try:
        result = subprocess.run(command, cwd="app", check=True)
        
        # Check both relative and absolute paths
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Audio generated successfully!")
            print(f"📁 File: {output_path}")
            print(f"📊 Size: {file_size} bytes")
            print(f"🕐 Created: {time.ctime(os.path.getmtime(output_path))}")
        elif os.path.exists(abs_output_path):
            file_size = os.path.getsize(abs_output_path)
            print(f"✅ Audio generated successfully (absolute path)!")
            print(f"📁 File: {abs_output_path}")
            print(f"📊 Size: {file_size} bytes")
            print(f"🕐 Created: {time.ctime(os.path.getmtime(abs_output_path))}")
        else:
            print(f"❌ Audio file was not created!")
            print(f"Checked paths:")
            print(f"  - {output_path}")
            print(f"  - {abs_output_path}")
            
            # List all files in audio directory for debugging
            audio_dir = "app/audio"
            if os.path.exists(audio_dir):
                print(f"Files in {audio_dir}:")
                for file in os.listdir(audio_dir):
                    print(f"  - {file}")
            return False
            
        # Also check the main output file
        main_output = "app/audio/output_tts.wav"
        if os.path.exists(main_output):
            main_size = os.path.getsize(main_output)
            main_time = time.ctime(os.path.getmtime(main_output))
            print(f"\n📁 Main output file: {main_output}")
            print(f"📊 Size: {main_size} bytes")
            print(f"🕐 Modified: {main_time}")
        
        return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Audio generation failed: {e}")
        return False

if __name__ == "__main__":
    test_audio_generation()
