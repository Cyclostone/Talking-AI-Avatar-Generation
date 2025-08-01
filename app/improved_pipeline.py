import os
import subprocess
import sys
import shlex
import time
import asyncio
import glob
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

class ImprovedAvatarPipeline:
    """
    Improved Avatar Pipeline - Based on working original with minimal optimizations
    
    Key improvements:
    - Async audio generation (non-blocking)
    - Better error handling
    - Progress tracking
    - Automatic cleanup of old files
    - Maintains original SadTalker approach that was working
    """
    
    def __init__(self, keep_files: int = 3):
        print("🚀 Initializing Improved Avatar Pipeline...")
        
        # Setup paths (same as original)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.audio_dir = os.path.join(self.project_root, "app", "audio")
        self.video_dir = os.path.join(self.project_root, "app", "video")
        self.sadtalker_dir = os.path.join(self.project_root, "SadTalker")
        
        # Cleanup settings
        self.keep_files = keep_files  # Keep only the most recent N files
        
        # Create directories
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Clean up old files on initialization
        self._cleanup_old_files()
        
        print("✅ Improved Avatar Pipeline initialized")
    
    def _cleanup_old_files(self):
        """Clean up old audio and video files, keeping only the most recent ones"""
        print("🧹 Cleaning up old files...")
        
        # Clean audio files
        audio_files = glob.glob(os.path.join(self.audio_dir, "*.wav"))
        audio_files.extend(glob.glob(os.path.join(self.audio_dir, "*.mp3")))
        
        if len(audio_files) > self.keep_files:
            # Sort by modification time (newest first)
            audio_files.sort(key=os.path.getmtime, reverse=True)
            files_to_remove = audio_files[self.keep_files:]
            
            for file_path in files_to_remove:
                try:
                    os.remove(file_path)
                    print(f"   🗑️ Removed old audio: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"   ⚠️ Could not remove {file_path}: {e}")
        
        # Clean video files and directories
        video_items = []
        
        # Get all .mp4 files
        for file_path in glob.glob(os.path.join(self.video_dir, "*.mp4")):
            video_items.append(('file', file_path, os.path.getmtime(file_path)))
        
        # Get all timestamp directories (e.g., 2025_07_31_20.11.27)
        for item in os.listdir(self.video_dir):
            item_path = os.path.join(self.video_dir, item)
            if os.path.isdir(item_path) and item.replace('_', '').replace('.', '').isdigit():
                video_items.append(('dir', item_path, os.path.getmtime(item_path)))
        
        if len(video_items) > self.keep_files:
            # Sort by modification time (newest first)
            video_items.sort(key=lambda x: x[2], reverse=True)
            items_to_remove = video_items[self.keep_files:]
            
            for item_type, item_path, _ in items_to_remove:
                try:
                    if item_type == 'file':
                        os.remove(item_path)
                        print(f"   🗑️ Removed old video: {os.path.basename(item_path)}")
                    elif item_type == 'dir':
                        import shutil
                        shutil.rmtree(item_path)
                        print(f"   🗑️ Removed old video dir: {os.path.basename(item_path)}")
                except Exception as e:
                    print(f"   ⚠️ Could not remove {item_path}: {e}")
        
        print("✨ Cleanup completed")
    
    async def generate_voice_async(self, text: str) -> str:
        """Generate audio using Google TTS (async version of original)"""
        print(f"🎵 Starting audio generation for text: '{text}'")
        
        # Generate unique filename with timestamp
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        audio_filename = f"audio_{timestamp}.wav"
        audio_path = os.path.join(self.audio_dir, audio_filename)
        
        print(f"📁 Audio directory: {self.audio_dir}")
        print(f"📁 Audio file path: {audio_path}")
        
        # Run the gTTS script with absolute paths
        script_path = os.path.join(self.project_root, "app", "generate_audio_gtts.py")
        command = [
            "python", script_path,
            "--text", text,
            "--output", audio_path
        ]
        
        print(f"Running command: {' '.join(shlex.quote(str(arg)) for arg in command)}")
        
        # Run in thread pool to make it async
        loop = asyncio.get_event_loop()
        
        try:
            await loop.run_in_executor(
                self.executor,
                lambda: subprocess.run(
                    command,
                    check=True,
                    cwd=self.project_root
                )
            )
            
            # Check if new file was created
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"✅ New audio file created: {audio_filename}")
                print(f"📊 Audio file size: {file_size} bytes")
            else:
                print(f"❌ Audio file was not created at: {audio_path}")
                raise RuntimeError("Audio file not created")
                
            print(f"✅ Audio generation completed!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Audio generation failed with return code {e.returncode}")
            raise
        
        # Return relative path for compatibility with SadTalker
        return f"app/audio/{audio_filename}"
    
    async def generate_video_async(self, audio_filename: str) -> str:
        """Generate video using SadTalker (async version of original)"""
        print(f"🎬 Starting video generation using SadTalker...")
        
        # Use the exact same command as the working original
        command = [
            "python", "inference.py",
            "--driven_audio", f"../{audio_filename}",
            "--source_image", "examples/source_image/art_3.png",  # Known working image
            "--result_dir", "../app/video",
            "--enhancer", "gfpgan",  # Same as original
            "--still",  # Same as original
            "--preprocess", "full"  # Same as original
        ]
        
        print(f"Running SadTalker: {' '.join(command)}")
        
        # Run in thread pool to make it async
        loop = asyncio.get_event_loop()
        
        try:
            await loop.run_in_executor(
                self.executor,
                lambda: subprocess.run(command, cwd=self.sadtalker_dir, check=True)
            )
            
            print(f"✅ SadTalker video generation completed!")
            
            # Find the most recent video file (same as original)
            video_files = []
            for root, dirs, files in os.walk(self.video_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        video_files.append(os.path.join(root, file))
            
            if video_files:
                # Return the most recently created video
                latest_video = max(video_files, key=os.path.getctime)
                print(f"📹 Found generated video: {latest_video}")
                return latest_video
            else:
                raise RuntimeError("No video file found after SadTalker generation")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ SadTalker generation failed with return code {e.returncode}")
            raise
    
    async def generate_avatar_video(self, text: str) -> Dict[str, str]:
        """
        Main pipeline function - improved version of original
        """
        pipeline_start = time.time()
        print(f"🚀 Starting improved avatar pipeline...")
        print(f"📝 Text: '{text}'")
        
        try:
            # Step 1: Generate audio (async)
            print(f"🎵 Step 1: Generating audio...")
            audio_path = await self.generate_voice_async(text)
            
            # Step 2: Generate video (async)
            print(f"🎬 Step 2: Generating video...")
            video_path = await self.generate_video_async(audio_path)
            
            # Calculate total time
            total_time = time.time() - pipeline_start
            
            # Prepare result
            result = {
                "audio_path": audio_path,
                "video_path": os.path.relpath(video_path, self.project_root) if video_path else None,
                "avatar_path": "SadTalker/examples/source_image/art_3.png",
                "total_time": round(total_time, 3),
                "success": True,
                "quality": "HIGH",
                "backend": "SadTalker (Original Working Approach)"
            }
            
            print(f"🎉 Improved pipeline completed in {total_time:.3f}s")
            print(f"📊 Quality: ✅ HIGH (Original SadTalker)")
            print(f"📊 Approach: Minimal optimization of working system")
            
            # Clean up old files after successful generation
            self._cleanup_old_files()
            
            return result
            
        except Exception as e:
            error_time = time.time() - pipeline_start
            print(f"❌ Improved pipeline failed after {error_time:.3f}s: {e}")
            
            return {
                "error": str(e),
                "total_time": round(error_time, 3),
                "success": False,
                "quality": "HIGH",
                "backend": "SadTalker (Original Working Approach)"
            }

# Convenience function for direct usage
async def generate_talking_avatar_improved(text: str) -> Dict[str, str]:
    """
    Convenience function for generating high-quality talking avatars
    Uses the improved version of the original working pipeline
    
    Args:
        text: Text to speak
    
    Returns:
        Dictionary with audio_path, video_path, and performance metrics
    """
    pipeline = ImprovedAvatarPipeline()
    return await pipeline.generate_avatar_video(text)
