import os
import subprocess
import sys
import shlex
import time

def generate_voice(text):
    """Generate audio using Google TTS"""
    print(f"🎵 Starting audio generation for text: '{text}'")
    
    # Use absolute paths to avoid working directory issues
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(project_root, "app", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    audio_path = os.path.join(audio_dir, "output_tts.wav")
    
    print(f"📁 Audio directory: {audio_dir}")
    print(f"📁 Audio file path: {audio_path}")
    
    # Check if audio file exists and get timestamp
    if os.path.exists(audio_path):
        old_timestamp = os.path.getmtime(audio_path)
        print(f"📁 Existing audio file timestamp: {time.ctime(old_timestamp)}")
        # Remove old file to ensure fresh generation
        os.remove(audio_path)
        print(f"🗑️ Removed old audio file")
    
    # Run the gTTS script with absolute paths
    script_path = os.path.join(project_root, "app", "generate_audio_gtts.py")
    command = [
        "python", script_path,
        "--text", text,
        "--output", audio_path
    ]
    
    print(f"Running command: {' '.join(shlex.quote(str(arg)) for arg in command)}")
    
    # Run without changing working directory
    try:
        result = subprocess.run(
            command,
            check=True,  # This will raise an exception if the command fails
            cwd=project_root  # Run from project root
        )
        
        # Check if new file was created
        if os.path.exists(audio_path):
            new_timestamp = os.path.getmtime(audio_path)
            print(f"✅ New audio file created at: {time.ctime(new_timestamp)}")
            
            # Get file size for verification
            file_size = os.path.getsize(audio_path)
            print(f"📊 Audio file size: {file_size} bytes")
        else:
            print(f"❌ Audio file was not created at: {audio_path}")
            
        print(f"✅ Audio generation completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Audio generation failed with return code {e.returncode}")
        raise
    
    # Return relative path for compatibility with SadTalker
    return "app/audio/output_tts.wav"

def generate_video():
    """Generate video using SadTalker"""
    result_path = "app/video"
    os.makedirs(result_path, exist_ok=True)

    command = [
        "python", "inference.py",
        "--driven_audio", "../app/audio/output_tts.wav",
        "--source_image", "examples/source_image/art_11.png",  # Use working example image
        "--result_dir", "../app/video",
        "--enhancer", "gfpgan",
        "--still",
        "--preprocess", "full"
    ]
    subprocess.run(command, cwd="SadTalker")
    
    # Return the generated video file (find the most recent one)
    video_files = []
    for root, dirs, files in os.walk(result_path):
        for file in files:
            if file.endswith('.mp4'):
                video_files.append(os.path.join(root, file))
    
    if video_files:
        # Return the most recently created video
        return max(video_files, key=os.path.getctime)
    return None