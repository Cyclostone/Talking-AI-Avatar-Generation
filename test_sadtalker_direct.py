#!/usr/bin/env python3
"""
Direct SadTalker Test - Debug the exact failure point
"""

import subprocess
import os
import sys
import time

def test_sadtalker_direct():
    """Test SadTalker command directly to capture exact error"""
    print("🔍 Direct SadTalker Test")
    print("=" * 50)
    
    # Setup paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    sadtalker_dir = os.path.join(project_root, "SadTalker")
    audio_dir = os.path.join(project_root, "app", "audio")
    
    print(f"Project root: {project_root}")
    print(f"SadTalker dir: {sadtalker_dir}")
    print(f"Audio dir: {audio_dir}")
    
    # Check if directories exist
    print(f"\nDirectory checks:")
    print(f"SadTalker exists: {os.path.exists(sadtalker_dir)}")
    print(f"Audio dir exists: {os.path.exists(audio_dir)}")
    
    # Check for inference.py
    inference_path = os.path.join(sadtalker_dir, "inference.py")
    print(f"inference.py exists: {os.path.exists(inference_path)}")
    
    # Check for default image
    default_image = os.path.join(sadtalker_dir, "examples", "source_image", "art_3.png")
    print(f"Default image exists: {os.path.exists(default_image)}")
    
    # Find latest audio file
    audio_files = []
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith('.mp3'):
                audio_files.append(os.path.join(audio_dir, file))
    
    if not audio_files:
        print("❌ No audio files found")
        return
    
    latest_audio = max(audio_files, key=os.path.getctime)
    audio_rel_path = os.path.relpath(latest_audio, sadtalker_dir)
    
    print(f"\nUsing audio: {latest_audio}")
    print(f"Relative path: {audio_rel_path}")
    print(f"Audio exists: {os.path.exists(latest_audio)}")
    
    # Prepare command
    command = [
        "python", "inference.py",
        "--driven_audio", audio_rel_path,
        "--source_image", "examples/source_image/art_3.png",
        "--result_dir", "../app/video",
        "--still",
        "--preprocess", "crop",
        "--size", "256",  # Use available 256px model instead of missing 128px
        "--batch_size", "1"
    ]
    
    print(f"\nCommand: {' '.join(command)}")
    print(f"Working directory: {sadtalker_dir}")
    
    # Test Python environment in SadTalker directory
    print(f"\n🐍 Testing Python environment...")
    try:
        env_test = subprocess.run(
            ["python", "--version"],
            cwd=sadtalker_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"Python version: {env_test.stdout.strip()}")
        print(f"Python stderr: {env_test.stderr.strip()}")
    except Exception as e:
        print(f"Python test failed: {e}")
    
    # Test imports
    print(f"\n📦 Testing key imports...")
    test_imports = [
        "import torch; print(f'PyTorch: {torch.__version__}')",
        "import numpy; print(f'NumPy: {numpy.__version__}')",
        "from src.utils.preprocess import CropAndExtract; print('CropAndExtract: OK')",
        "from src.test_audio2coeff import Audio2Coeff; print('Audio2Coeff: OK')"
    ]
    
    for test_cmd in test_imports:
        try:
            result = subprocess.run(
                ["python", "-c", test_cmd],
                cwd=sadtalker_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
            else:
                print(f"❌ Import failed: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Import test failed: {e}")
    
    # Run the actual SadTalker command
    print(f"\n🎬 Running SadTalker command...")
    try:
        start_time = time.time()
        
        process = subprocess.Popen(
            command,
            cwd=sadtalker_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"Process started with PID: {process.pid}")
        
        # Wait for completion with timeout
        try:
            stdout, stderr = process.communicate(timeout=30)
            elapsed = time.time() - start_time
            
            print(f"\n📊 Results:")
            print(f"Return code: {process.returncode}")
            print(f"Elapsed time: {elapsed:.2f}s")
            print(f"STDOUT length: {len(stdout)} chars")
            print(f"STDERR length: {len(stderr)} chars")
            
            if stdout:
                print(f"\n📤 STDOUT:")
                print(stdout[:1000] + ("..." if len(stdout) > 1000 else ""))
            
            if stderr:
                print(f"\n📤 STDERR:")
                print(stderr[:1000] + ("..." if len(stderr) > 1000 else ""))
            
            if process.returncode == 0:
                print("✅ SadTalker completed successfully!")
            else:
                print(f"❌ SadTalker failed with return code {process.returncode}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Process timed out after 30 seconds")
            process.kill()
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Timeout STDERR: {stderr}")
    
    except Exception as e:
        print(f"❌ Failed to start process: {e}")

if __name__ == "__main__":
    test_sadtalker_direct()
