import os
import subprocess
import sys
import shlex
import time
import asyncio
import glob
import torch
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Callable
import streamlit as st
from tqdm import tqdm

class ProgressTracker:
    """Real-time progress tracking with loading bars"""
    
    def __init__(self, total_steps: int = 100):
        self.total_steps = total_steps
        self.current_step = 0
        self.step_name = "Initializing..."
        self.start_time = time.time()
        self.step_times = []
        
        # Streamlit progress elements
        self.progress_bar = None
        self.status_text = None
        self.time_text = None
        
    def setup_streamlit_ui(self):
        """Setup Streamlit progress UI elements"""
        if 'st' in globals():
            self.progress_bar = st.progress(0)
            self.status_text = st.empty()
            self.time_text = st.empty()
            
    def update(self, step: int, step_name: str, details: str = ""):
        """Update progress with step information"""
        self.current_step = step
        self.step_name = step_name
        
        # Calculate progress percentage
        progress = min(step / self.total_steps, 1.0)
        elapsed = time.time() - self.start_time
        
        # Estimate remaining time
        if step > 0:
            avg_time_per_step = elapsed / step
            remaining_steps = self.total_steps - step
            eta = avg_time_per_step * remaining_steps
            eta_str = f" (ETA: {eta:.1f}s)" if eta > 0 else ""
        else:
            eta_str = ""
        
        # Update UI elements
        if self.progress_bar:
            self.progress_bar.progress(progress)
        if self.status_text:
            self.status_text.text(f" {step_name} {details}")
        if self.time_text:
            self.time_text.text(f" {elapsed:.1f}s elapsed{eta_str}")
            
        # Console output
        print(f"[{step:3d}/{self.total_steps}] {step_name} {details}")
        
    def complete(self, success: bool = True):
        """Mark progress as complete"""
        total_time = time.time() - self.start_time
        if success:
            if self.status_text:
                self.status_text.text(f" Pipeline completed successfully!")
            if self.time_text:
                self.time_text.text(f" Total time: {total_time:.2f}s")
            print(f" Pipeline completed in {total_time:.2f}s")
        else:
            if self.status_text:
                self.status_text.text(f" Pipeline failed")
            print(f" Pipeline failed after {total_time:.2f}s")

class UltraOptimizedPipeline:
    """
    Ultra-Optimized Avatar Pipeline with Aggressive Speed Improvements
    
    Key Optimizations:
    1. Minimal resolution (256x256) for maximum speed
    2. Skip all enhancement steps
    3. Use fastest preprocessing
    4. Aggressive memory management
    5. Real-time progress tracking
    6. Parallel processing where possible
    """
    
    def __init__(self, keep_files: int = 2):
        print(" Initializing Ultra-Optimized Pipeline...")
        
        # Setup paths
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.audio_dir = os.path.join(self.project_root, "app", "audio")
        self.video_dir = os.path.join(self.project_root, "app", "video")
        self.sadtalker_dir = os.path.join(self.project_root, "SadTalker")
        
        # Ultra-aggressive settings
        self.keep_files = keep_files
        
        # Create directories
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # Single thread for maximum resource focus
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Setup ultra-optimized environment
        self._setup_ultra_optimization()
        
        # Aggressive cleanup
        self._aggressive_cleanup()
        
        print(" Ultra-Optimized Pipeline initialized")
    
    def _setup_ultra_optimization(self):
        """Setup ultra-aggressive optimization environment"""
        print(" Setting up ultra-optimization environment...")
        
        # Check GPU
        if torch.cuda.is_available():
            self.device = "cuda"
            print(f"   CUDA GPU detected")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            self.device = "mps"
            print(f"   Apple MPS detected")
        else:
            self.device = "cpu"
            print(f"   CPU mode")
        
        # Ultra-aggressive environment variables
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"
        os.environ["OMP_NUM_THREADS"] = "2"  # Minimal CPU threads
        os.environ["CUDA_LAUNCH_BLOCKING"] = "0"  # Async CUDA
        os.environ["PYTHONUNBUFFERED"] = "1"  # Immediate output
        
        print(f"   Ultra-optimization mode: MAXIMUM SPEED")
        print(f"   Target: Sub-60 second generation")
    
    def _aggressive_cleanup(self):
        """Aggressive cleanup of all old files"""
        print(" Aggressive cleanup...")
        
        # Remove ALL old files except most recent
        for directory in [self.audio_dir, self.video_dir]:
            all_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append((file_path, os.path.getmtime(file_path)))
            
            if len(all_files) > self.keep_files:
                all_files.sort(key=lambda x: x[1], reverse=True)
                for file_path, _ in all_files[self.keep_files:]:
                    try:
                        os.remove(file_path)
                    except:
                        pass
        
        print(" Aggressive cleanup completed")
    
    async def generate_voice_ultra_fast(self, text: str, progress: ProgressTracker) -> str:
        """Ultra-fast audio generation with progress tracking"""
        progress.update(10, "Audio Generation", "Starting TTS...")
        
        try:
            from gtts import gTTS
            import io
            
            # Truncate text for speed
            text = text[:200] if len(text) > 200 else text
            progress.update(15, "Audio Generation", f"Processing {len(text)} chars...")
            
            # Generate audio with minimal settings
            tts = gTTS(text=text, lang='en', slow=False)
            progress.update(20, "Audio Generation", "Generating audio...")
            
            # Save audio
            timestamp = int(time.time() * 1000)
            audio_filename = f"audio_{timestamp}.mp3"
            audio_path = os.path.join(self.audio_dir, audio_filename)
            
            tts.save(audio_path)
            progress.update(25, "Audio Generation", "Audio saved")
            
            audio_size = os.path.getsize(audio_path)
            print(f"   Audio: {audio_size:,} bytes")
            
            return audio_path
            
        except Exception as e:
            print(f"   Audio generation failed: {e}")
            raise
    
    def _get_ultra_fast_command(self, audio_filename: str, image_path: str = None) -> list:
        """Get ultra-fast SadTalker command with minimal settings"""
        
        # Fix audio path - use relative path from SadTalker directory
        audio_rel_path = os.path.relpath(audio_filename, self.sadtalker_dir)
        
        # Use custom image if provided, otherwise fallback to default
        if image_path and os.path.exists(image_path):
            # Convert to relative path from SadTalker directory
            image_rel_path = os.path.relpath(image_path, self.sadtalker_dir)
            print(f"   Using custom image: {image_path}")
        else:
            # Fallback to default image for ultra-fast processing
            image_rel_path = "examples/source_image/art_3.png"
            print(f"   Using default image for ultra-fast processing")
        
        command = [
            "python", "inference.py",
            "--driven_audio", audio_rel_path,
            "--source_image", image_rel_path,
            "--result_dir", "../app/video",
            "--still",  # Fastest mode
            "--preprocess", "crop",  # Fastest preprocessing
            "--size", "256",  # Use available 256px model instead of missing 128px
            "--batch_size", "1",  # Minimal batch
            # Skip ALL enhancement for maximum speed
        ]
        
        # Add CPU flag if needed
        if self.device == "cpu":
            command.append("--cpu")
        
        print(f"   Ultra-fast command: {' '.join(command)}")
        return command
    
    async def generate_video_ultra_fast(self, audio_filename: str, progress: ProgressTracker, image_path: str = None) -> str:
        """Ultra-fast video generation with progress tracking"""
        progress.update(30, "Video Generation", "Preparing SadTalker...")
        
        # Get ultra-fast command
        command = self._get_ultra_fast_command(audio_filename, image_path)
        
        progress.update(35, "Video Generation", "Starting SadTalker process...")
        print(f"   Device: {self.device.upper()}")
        print(f"   Mode: ULTRA-FAST (256px, no enhancement)")
        print(f"   Working directory: {self.sadtalker_dir}")
        print(f"   Command: {' '.join(command)}")
        
        # Run with progress monitoring
        loop = asyncio.get_event_loop()
        
        def run_with_progress():
            try:
                process = subprocess.Popen(
                    command,
                    cwd=self.sadtalker_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                print(f"   Process started with PID: {process.pid}")
                
                # Wait for completion with NO timeout - let it run to completion
                try:
                    stdout, stderr = process.communicate()  # No timeout - let it complete naturally
                    print(f"   Process completed with return code: {process.returncode}")
                    
                    # Enhanced error reporting
                    if stdout:
                        print(f"   STDOUT: {stdout[:200]}...")
                    if stderr:
                        print(f"   STDERR: {stderr[:500]}...")
                    
                    if process.returncode != 0:
                        error_msg = f"SadTalker failed with return code {process.returncode}"
                        if stderr:
                            error_msg += f"\nSTDERR: {stderr}"
                        raise subprocess.CalledProcessError(process.returncode, command, error_msg)
                    return stdout, stderr
                    
                except Exception as e:
                    print(f"   Process error: {str(e)}")
                    raise e
            except Exception as e:
                print(f"   Failed to start SadTalker process: {str(e)}")
                raise e
        
        try:
            stdout, stderr = await loop.run_in_executor(self.executor, run_with_progress)
            progress.update(95, "Video Generation", "Finding output video...")
            
            # Find the most recent video file
            video_files = []
            for root, dirs, files in os.walk(self.video_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        video_files.append(os.path.join(root, file))
            
            if video_files:
                latest_video = max(video_files, key=os.path.getctime)
                video_size = os.path.getsize(latest_video)
                progress.update(98, "Video Generation", f"Video ready ({video_size:,} bytes)")
                print(f"   Video: {video_size:,} bytes")
                return latest_video
            else:
                # Check if any files were created
                print(f"   No video files found in {self.video_dir}")
                print(f"   Directory contents: {os.listdir(self.video_dir) if os.path.exists(self.video_dir) else 'Directory does not exist'}")
                raise RuntimeError("No video file found after SadTalker execution")
                
        except subprocess.CalledProcessError as e:
            print(f"   SadTalker subprocess failed: {e}")
            print(f"   Command that failed: {' '.join(command)}")
            raise RuntimeError(f"SadTalker execution failed: {e}")
        except Exception as e:
            print(f"   Unexpected error in video generation: {e}")
            raise
    
    async def generate_avatar_video(self, text: str, image_path: str = None, progress_callback: Callable = None) -> Dict[str, str]:
        """
        Ultra-optimized pipeline with comprehensive progress tracking
        """
        pipeline_start = time.time()
        
        # Setup progress tracker
        progress = ProgressTracker(total_steps=100)
        if progress_callback:
            progress_callback(progress)
        
        progress.update(0, "Initialization", "Starting ultra-optimized pipeline...")
        print(f" Starting ultra-optimized avatar pipeline...")
        print(f" Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f" Target: Maximum speed with minimal quality trade-offs")
        
        try:
            # Step 1: Ultra-fast audio generation
            progress.update(5, "Audio Generation", "Initializing TTS...")
            audio_start = time.time()
            audio_path = await self.generate_voice_ultra_fast(text, progress)
            audio_time = time.time() - audio_start
            
            # Step 2: Ultra-fast video generation
            video_start = time.time()
            video_path = await self.generate_video_ultra_fast(audio_path, progress, image_path)
            video_time = time.time() - video_start
            
            # Calculate total time
            total_time = time.time() - pipeline_start
            
            progress.update(99, "Finalizing", "Preparing results...")
            
            # Verify output
            if video_path and os.path.exists(video_path):
                video_size = os.path.getsize(video_path)
                quality_check = "SPEED_OPTIMIZED"
            else:
                quality_check = "ERROR"
            
            # Calculate speedup from baseline
            baseline_time = 7519.0  # From previous slow run
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
                "quality_mode": "ultra_fast",
                "speedup": round(speedup, 1),
                "backend": f"Ultra-Optimized SadTalker ({self.device.upper()})",
                "optimization_level": "MAXIMUM",
                "target_achieved": total_time < 60.0,
                "performance_notes": f"{speedup:.1f}x faster than baseline"
            }
            
            progress.update(100, "Complete", f"Generated in {total_time:.1f}s!")
            progress.complete(success=True)
            
            print(f"\n Ultra-optimized pipeline completed!")
            print(f"   Total: {total_time:.2f}s")
            print(f"   Audio: {audio_time:.2f}s")
            print(f"   Video: {video_time:.2f}s")
            print(f"   Speedup: {speedup:.1f}x faster than baseline")
            print(f"   Target achieved: {' YES' if total_time < 60.0 else ' NO'}")
            
            # Cleanup after success
            self._aggressive_cleanup()
            
            return result
            
        except Exception as e:
            error_time = time.time() - pipeline_start
            progress.complete(success=False)
            print(f"\n Ultra-optimized pipeline failed after {error_time:.2f}s: {e}")
            
            return {
                "error": str(e),
                "total_time": round(error_time, 3),
                "success": False,
                "quality": "ERROR",
                "backend": f"Ultra-Optimized SadTalker ({self.device.upper()})",
                "optimization_level": "MAXIMUM"
            }

# Convenience functions
async def generate_ultra_fast_avatar(text: str, image_path: str = None, progress_callback: Callable = None) -> Dict[str, str]:
    """
    Ultra-fast avatar generation with progress tracking
    
    Args:
        text: Text to speak
        image_path: Optional custom image path
        progress_callback: Optional callback to receive ProgressTracker instance
    
    Returns:
        Dictionary with results and performance metrics
    """
    pipeline = UltraOptimizedPipeline()
    return await pipeline.generate_avatar_video(text, image_path, progress_callback)

async def generate_ultra_fast_avatar_with_timing(text: str, image_path: str = None, progress_elements: dict = None) -> dict:
    """
    Generate talking avatar with ultra-fast optimizations and comprehensive progress tracking
    
    Returns:
        dict: Results with timing information, success status, and file paths
    """
    pipeline_start_time = time.time()
    print(f"\n Starting ultra-optimized avatar pipeline...")
    print(f"   Text: '{text}'")
    print(f"   Target: Maximum speed with minimal quality trade-offs")
    
    # Initialize progress tracker
    progress = ProgressTracker(
        progress_bar=progress_elements.get('progress_bar') if progress_elements else None,
        status_text=progress_elements.get('status_text') if progress_elements else None,
        time_text=progress_elements.get('time_text') if progress_elements else None,
        details_text=progress_elements.get('details_text') if progress_elements else None,
        start_time=pipeline_start_time
    )
    
    try:
        # Initialize pipeline
        progress.update(0, "Initialization", "Starting ultra-optimized pipeline...")
        pipeline = UltraOptimizedPipeline()
        
        # Audio generation
        progress.update(5, "Audio Generation", "Initializing TTS...")
        audio_start_time = time.time()
        audio_filename = await pipeline.generate_voice_ultra_fast(text, progress)
        audio_end_time = time.time()
        audio_time = audio_end_time - audio_start_time
        
        # Video generation
        progress.update(30, "Video Generation", "Preparing SadTalker...")
        video_start_time = time.time()
        video_filename = await pipeline.generate_video_ultra_fast(audio_filename, progress, image_path)
        video_end_time = time.time()
        video_time = video_end_time - video_start_time
        
        # Complete
        pipeline_end_time = time.time()
        total_time = pipeline_end_time - pipeline_start_time
        
        progress.update(100, "Complete", f"Pipeline completed in {total_time:.2f}s!")
        
        # Calculate speedup vs baseline (7519 seconds)
        baseline_time = 7519
        speedup = baseline_time / total_time if total_time > 0 else 0
        target_achieved = total_time < 60
        
        print(f"\n ULTRA-OPTIMIZED PIPELINE COMPLETE!")
        print(f"   TOTAL TIME: {total_time:.2f} seconds")
        print(f"   Audio time: {audio_time:.2f}s")
        print(f"   Video time: {video_time:.2f}s")
        print(f"   Speedup: {speedup:.1f}x faster than baseline")
        print(f"   Target (<60s): {' ACHIEVED' if target_achieved else ' MISSED'}")
        
        return {
            "success": True,
            "audio_file": audio_filename,
            "video_file": video_filename,
            "total_time": total_time,
            "audio_time": audio_time,
            "video_time": video_time,
            "speedup": speedup,
            "target_achieved": target_achieved,
            "baseline_time": baseline_time,
            "backend": "Ultra-Optimized SadTalker"
        }
        
    except Exception as e:
        pipeline_end_time = time.time()
        total_time = pipeline_end_time - pipeline_start_time
        
        print(f"\n Ultra-optimized pipeline failed after {total_time:.2f}s: {str(e)}")
        
        return {
            "success": False,
            "error": str(e),
            "total_time": total_time,
            "audio_time": 0,
            "video_time": 0,
            "speedup": 0,
            "target_achieved": False,
            "baseline_time": 7519,
            "backend": "Ultra-Optimized SadTalker"
        }

def setup_streamlit_progress_ui():
    """Setup Streamlit UI for progress tracking"""
    st.markdown("### Ultra-Optimized Pipeline Progress")
    
    # Create placeholder containers
    progress_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        time_text = st.empty()
        details_text = st.empty()
    
    return {
        'progress_bar': progress_bar,
        'status_text': status_text,
        'time_text': time_text,
        'details_text': details_text
    }
