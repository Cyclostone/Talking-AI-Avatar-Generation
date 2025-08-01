#!/usr/bin/env python3
"""
Direct test script to measure SadTalker 256px model completion time
"""

import subprocess
import time
import os

def test_sadtalker_256px_timing():
    """Test SadTalker with 256px model and measure completion time"""
    
    print("🚀 Testing SadTalker 256px Model Timing")
    print("=" * 50)
    
    # Setup paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    sadtalker_dir = os.path.join(project_root, "SadTalker")
    audio_dir = os.path.join(project_root, "app", "audio")
    
    # Find latest audio file
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    if not audio_files:
        print("❌ No audio files found")
        return
    
    latest_audio = sorted(audio_files)[-1]
    audio_path = f"../app/audio/{latest_audio}"
    
    print(f"Audio file: {latest_audio}")
    print(f"Working directory: {sadtalker_dir}")
    
    # Command with 256px model
    command = [
        "python", "inference.py",
        "--driven_audio", audio_path,
        "--source_image", "examples/source_image/art_3.png",
        "--result_dir", "../app/video",
        "--still",
        "--preprocess", "crop",
        "--size", "256",  # Use available 256px model
        "--batch_size", "1"
    ]
    
    print(f"Command: {' '.join(command)}")
    print("\n🎬 Starting SadTalker process...")
    
    # Measure timing
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            cwd=sadtalker_dir,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n📊 RESULTS:")
        print(f"   Return code: {result.returncode}")
        print(f"   Elapsed time: {elapsed_time:.2f} seconds")
        
        if result.stdout:
            print(f"   STDOUT: {result.stdout[:300]}...")
        
        if result.stderr:
            print(f"   STDERR: {result.stderr[:500]}...")
        
        if result.returncode == 0:
            print(f"\n✅ SUCCESS! SadTalker 256px completed in {elapsed_time:.2f} seconds")
            
            # Calculate total pipeline time estimate
            audio_time = 0.3  # From previous tests
            total_time = audio_time + elapsed_time
            speedup = 7519 / total_time if total_time > 0 else 0
            
            print(f"\n🎉 ULTRA-OPTIMIZED PIPELINE PROJECTION:")
            print(f"   🎵 Audio time: {audio_time:.2f}s")
            print(f"   🎬 Video time: {elapsed_time:.2f}s")
            print(f"   📊 TOTAL TIME: {total_time:.2f} seconds")
            print(f"   🚀 Speedup: {speedup:.1f}x faster than baseline (7519s)")
            print(f"   🎯 Target (<60s): {'✅ ACHIEVED' if total_time < 60 else '❌ MISSED'}")
            
        else:
            print(f"\n❌ FAILED with return code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\n⏰ TIMEOUT after {elapsed_time:.2f} seconds")
        
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\n❌ ERROR after {elapsed_time:.2f} seconds: {e}")

if __name__ == "__main__":
    test_sadtalker_256px_timing()
