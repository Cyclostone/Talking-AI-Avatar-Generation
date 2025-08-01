import os
import subprocess
import sys
import shlex
import time
import asyncio
import glob
import torch
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

class OptimizedSadTalkerPipeline:
    """
    Aggressively Optimized SadTalker Pipeline
    
    Targets the actual bottlenecks observed in GPU testing:
    - Face Renderer: 9+ minutes → optimize with faster settings
    - Face Enhancer: 4+ minutes → make optional/faster
    - Model loading: optimize with caching
    - Resolution: optimize for speed vs quality balance
    """
    
    def __init__(self, keep_files: int = 3, quality_mode: str = "balanced"):
        print("🚀 Initializing Optimized SadTalker Pipeline...")
        
        # Setup paths
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.audio_dir = os.path.join(self.project_root, "app", "audio")
        self.video_dir = os.path.join(self.project_root, "app", "video")
        self.sadtalker_dir = os.path.join(self.project_root, "SadTalker")
        
        # Optimization settings
        self.keep_files = keep_files
        self.quality_mode = quality_mode  # "fast", "balanced", "high"
        
        # Create directories
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Setup GPU and optimization environment
        self._setup_optimization_environment()
        
        # Clean up old files
        self._cleanup_old_files()
        
        print("✅ Optimized SadTalker Pipeline initialized")
    
    def _setup_optimization_environment(self):
        """Setup optimization environment for maximum speed"""
        print("🔧 Setting up optimization environment...")
        
        # Check GPU availability
        if torch.cuda.is_available():
            self.device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            print(f"   ✅ CUDA GPU: {gpu_name}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            self.device = "mps"
            print(f"   ✅ Apple MPS detected")
        else:
            self.device = "cpu"
            print(f"   ⚠️ CPU mode")
        
        # Set aggressive optimization environment variables
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"  # Reduce overhead
        os.environ["OMP_NUM_THREADS"] = "4"  # Optimize CPU threads
        
        print(f"   🚀 Optimization mode: {self.quality_mode}")
        print(f"   🎯 Target: Aggressive speed optimization")
    
    def _cleanup_old_files(self):
        """Clean up old files efficiently"""
        print("🧹 Cleaning up old files...")
        
        # Clean audio files
        audio_files = glob.glob(os.path.join(self.audio_dir, "*.wav"))
        audio_files.extend(glob.glob(os.path.join(self.audio_dir, "*.mp3")))
        
        if len(audio_files) > self.keep_files:
            audio_files.sort(key=os.path.getmtime, reverse=True)
            for file_path in audio_files[self.keep_files:]:
                try:
                    os.remove(file_path)
                except:
                    pass
        
        # Clean video files and directories
        video_items = []
        
        for file_path in glob.glob(os.path.join(self.video_dir, "*.mp4")):
            video_items.append(('file', file_path, os.path.getmtime(file_path)))
        
        for item in os.listdir(self.video_dir):
            item_path = os.path.join(self.video_dir, item)
            if os.path.isdir(item_path):
                video_items.append(('dir', item_path, os.path.getmtime(item_path)))
        
        if len(video_items) > self.keep_files:
            video_items.sort(key=lambda x: x[2], reverse=True)
            for item_type, item_path, _ in video_items[self.keep_files:]:
                try:
                    if item_type == 'file':
                        os.remove(item_path)
                    elif item_type == 'dir':
                        import shutil
                        shutil.rmtree(item_path)
                except:
                    pass
        
        print("✨ Cleanup completed")
    
    async def generate_voice_async(self, text: str) -> str:
        """Generate audio using optimized gTTS"""
        print(f"🎵 Starting optimized audio generation...")
        
        # Generate unique filename with timestamp
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        audio_filename = f"audio_{timestamp}.wav"
        audio_path = os.path.join(self.audio_dir, audio_filename)
        
        # Run the gTTS script
        script_path = os.path.join(self.project_root, "app", "generate_audio_gtts.py")
        command = [
            "python", script_path,
            "--text", text,
            "--output", audio_path
        ]
        
        print(f"   📝 Text length: {len(text)} characters")
        
        # Run in thread pool
        loop = asyncio.get_event_loop()
        
        try:
            await loop.run_in_executor(
                self.executor,
                lambda: subprocess.run(
                    command,
                    check=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
            )
            
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"   ✅ Audio: {file_size:,} bytes")
            else:
                raise RuntimeError("Audio file not created")
                
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Audio failed: {e.stderr}")
            raise
        
        return f"app/audio/{audio_filename}"
    
    def _get_optimized_sadtalker_command(self, audio_filename: str) -> list:
        """Get optimized SadTalker command based on quality mode"""
        
        base_command = [
            "python", "inference.py",
            "--driven_audio", f"../{audio_filename}",
            "--source_image", "examples/source_image/art_3.png",
            "--result_dir", "../app/video",
        ]
        
        if self.quality_mode == "fast":
            # Maximum speed optimizations
            command = base_command + [
                "--still",  # Faster processing
                "--preprocess", "crop",  # Faster than "full"
                "--size", "256",  # Smaller resolution for speed
                # Skip enhancer for maximum speed
            ]
            print(f"   ⚡ FAST mode: Maximum speed, good quality")
            
        elif self.quality_mode == "balanced":
            # Balanced speed/quality
            command = base_command + [
                "--still",  # Faster processing
                "--preprocess", "crop",  # Faster preprocessing
                "--enhancer", "gfpgan",  # Keep enhancement but optimize
                "--size", "512",  # Moderate resolution
            ]
            print(f"   ⚖️ BALANCED mode: Speed + quality balance")
            
        else:  # high quality
            # High quality (closer to original)
            command = base_command + [
                "--preprocess", "full",  # Full preprocessing
                "--enhancer", "gfpgan",  # Full enhancement
                # Default size for high quality
            ]
            print(f"   🏆 HIGH mode: Maximum quality")
        
        # Add CPU flag if no GPU
        if self.device == "cpu":
            command.append("--cpu")
        
        return command
    
    async def generate_video_async(self, audio_filename: str) -> str:
        """Generate video using aggressively optimized SadTalker"""
        print(f"🎬 Starting optimized SadTalker ({self.quality_mode} mode)...")
        
        # Get optimized command
        command = self._get_optimized_sadtalker_command(audio_filename)
        
        print(f"   🚀 Device: {self.device.upper()}")
        print(f"   🎯 Mode: {self.quality_mode.upper()}")
        print(f"   ⚡ Command: {' '.join(command)}")
        
        # Run in thread pool
        loop = asyncio.get_event_loop()
        
        try:
            result = await loop.run_in_executor(
                self.executor,
                lambda: subprocess.run(
                    command, 
                    cwd=self.sadtalker_dir, 
                    check=True,
                    capture_output=True,
                    text=True
                )
            )
            
            print(f"   ✅ SadTalker optimization completed")
            
            # Find the most recent video file
            video_files = []
            for root, dirs, files in os.walk(self.video_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        video_files.append(os.path.join(root, file))
            
            if video_files:
                latest_video = max(video_files, key=os.path.getctime)
                video_size = os.path.getsize(latest_video)
                print(f"   📹 Video: {video_size:,} bytes")
                return latest_video
            else:
                raise RuntimeError("No video file found")
                
        except subprocess.CalledProcessError as e:
            print(f"   ❌ SadTalker failed: {e.stderr}")
            raise
    
    async def generate_avatar_video(self, text: str) -> Dict[str, str]:
        """
        Main optimized pipeline function
        """
        pipeline_start = time.time()
        print(f"🚀 Starting optimized SadTalker pipeline...")
        print(f"📝 Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"🎯 Mode: {self.quality_mode.upper()}")
        print(f"🏁 Target: Significant speedup from 959s baseline")
        
        try:
            # Step 1: Generate audio (already optimized)
            print(f"\n🎵 Step 1: Audio generation...")
            audio_start = time.time()
            audio_path = await self.generate_voice_async(text)
            audio_time = time.time() - audio_start
            print(f"   ⏱️ Audio: {audio_time:.2f}s")
            
            # Step 2: Generate video (aggressively optimized)
            print(f"\n🎬 Step 2: Optimized video generation...")
            video_start = time.time()
            video_path = await self.generate_video_async(audio_path)
            video_time = time.time() - video_start
            print(f"   ⏱️ Video: {video_time:.2f}s")
            
            # Calculate total time
            total_time = time.time() - pipeline_start
            
            # Verify quality
            if video_path and os.path.exists(video_path):
                video_size = os.path.getsize(video_path)
                if video_size > 200000:  # >200KB = good quality
                    quality_check = "HIGH"
                elif video_size > 50000:  # >50KB = acceptable
                    quality_check = "MODERATE"
                else:
                    quality_check = "LOW"
            else:
                quality_check = "ERROR"
            
            # Calculate speedup
            baseline_time = 959.0  # From previous test
            speedup = baseline_time / total_time if total_time > 0 else 0
            
            # Prepare result
            result = {
                "audio_path": audio_path,
                "video_path": os.path.relpath(video_path, self.project_root) if video_path else None,
                "avatar_path": "SadTalker/examples/source_image/art_3.png",
                "total_time": round(total_time, 3),
                "audio_time": round(audio_time, 3),
                "video_time": round(video_time, 3),
                "success": True,
                "quality": quality_check,
                "quality_mode": self.quality_mode,
                "speedup": round(speedup, 1),
                "backend": f"Optimized SadTalker ({self.device.upper()})",
                "daylily_target": "< 2 seconds",
                "daylily_status": "✅ ACHIEVED" if total_time < 2.0 else f"⏱️ {total_time:.1f}s ({speedup:.1f}x speedup)"
            }
            
            print(f"\n🎉 Optimized pipeline completed!")
            print(f"   ⏱️ Total: {total_time:.2f}s")
            print(f"   🚀 Speedup: {speedup:.1f}x faster than baseline")
            print(f"   🏆 Quality: {quality_check}")
            print(f"   🎯 Daylily: {result['daylily_status']}")
            
            # Clean up after successful generation
            self._cleanup_old_files()
            
            return result
            
        except Exception as e:
            error_time = time.time() - pipeline_start
            print(f"\n❌ Optimized pipeline failed after {error_time:.2f}s: {e}")
            
            return {
                "error": str(e),
                "total_time": round(error_time, 3),
                "success": False,
                "quality": "ERROR",
                "quality_mode": self.quality_mode,
                "backend": f"Optimized SadTalker ({self.device.upper()})",
                "daylily_status": "❌ FAILED"
            }

# Convenience functions for different quality modes
async def generate_fast_avatar(text: str) -> Dict[str, str]:
    """Fast mode: Maximum speed optimization"""
    pipeline = OptimizedSadTalkerPipeline(quality_mode="fast")
    return await pipeline.generate_avatar_video(text)

async def generate_balanced_avatar(text: str) -> Dict[str, str]:
    """Balanced mode: Speed + quality balance"""
    pipeline = OptimizedSadTalkerPipeline(quality_mode="balanced")
    return await pipeline.generate_avatar_video(text)

async def generate_high_quality_avatar(text: str) -> Dict[str, str]:
    """High quality mode: Maximum quality (slower)"""
    pipeline = OptimizedSadTalkerPipeline(quality_mode="high")
    return await pipeline.generate_avatar_video(text)
