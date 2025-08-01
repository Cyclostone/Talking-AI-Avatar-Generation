#!/usr/bin/env python3
"""
Streamlit Web App: AI Talking Avatar Generator
Upload a photo and enter text to generate a talking avatar using ultra-optimized SadTalker pipeline
"""

import streamlit as st
import asyncio
import os
import sys
import time
import tempfile
import shutil
from PIL import Image
import base64

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import our ultra-optimized pipeline
from ultra_optimized_pipeline import UltraOptimizedPipeline, ProgressTracker, generate_ultra_fast_avatar

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f0f8ff;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        background-color: #f0fff0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        background-color: #fff0f0;
    }
</style>
""", unsafe_allow_html=True)

def get_video_base64(video_path):
    """Convert video to base64 for embedding"""
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode()
            return video_base64
    except Exception as e:
        st.error(f"Error loading video: {e}")
        return None

def save_uploaded_image(uploaded_file, save_dir):
    """Save uploaded image to SadTalker source images directory"""
    try:
        # Create filename
        filename = f"uploaded_{int(time.time())}.png"
        save_path = os.path.join(save_dir, filename)
        
        # Save image
        image = Image.open(uploaded_file)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(save_path)
        
        return save_path, filename
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None, None

async def generate_talking_avatar_ultra_fast(image_path, text, progress_elements=None):
    """Generate talking avatar using ultra-optimized pipeline with progress tracking"""
    try:
        # Setup progress tracker
        progress_tracker = None
        
        def setup_progress(tracker):
            nonlocal progress_tracker
            progress_tracker = tracker
            if progress_elements:
                tracker.progress_bar = progress_elements['progress_bar']
                tracker.status_text = progress_elements['status_text']
                tracker.time_text = progress_elements['time_text']
        
        # Initialize ultra-optimized pipeline
        pipeline = UltraOptimizedPipeline()
        
        # Use custom image if provided, otherwise fallback to default
        if image_path and os.path.exists(image_path):
            print(f"   Using custom uploaded image: {image_path}")
        else:
            print(f"   Using default image for ultra-fast processing")
            print(f"   Custom image path (reference): {image_path}")
        
        # Generate avatar with progress tracking (using custom or default image)
        result = await pipeline.generate_avatar_video(text, image_path, setup_progress)
        
        return result
        
    except Exception as e:
        print(f"❌ Ultra-fast generation failed: {e}")
        return {
            "error": str(e),
            "success": False,
            "backend": "Ultra-Optimized SadTalker"
        }

def main():
    """Main Streamlit app"""
    # Header
    st.markdown('<h1 class="main-header">🎭 AI Talking Avatar Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform any photo into a talking avatar with ultra-fast optimization!</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Settings")
        
        # Quality mode selection (simplified for ultra-fast)
        st.subheader("⚡ Optimization Level")
        optimization_info = st.info("🚀 **Ultra-Fast Mode**: Maximum speed optimization with 128px resolution and no enhancement for sub-60 second generation")
        
        # Performance info
        st.subheader("📊 Performance Target")
        st.markdown("""
        - **Target**: < 60 seconds total
        - **Previous baseline**: 7519 seconds
        - **Expected speedup**: 100x+ faster
        - **Quality**: Speed-optimized
        """)
        
        # System info
        st.subheader("🖥️ System")
        import torch
        if torch.cuda.is_available():
            st.success("✅ CUDA GPU detected")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            st.success("✅ Apple MPS detected")
        else:
            st.warning("⚠️ CPU mode (slower)")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Upload Your Photo")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo with a visible face for best results"
        )
        
        if uploaded_file:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        st.subheader("💬 Enter Text")
        text_input = st.text_area(
            "What should your avatar say?",
            placeholder="Enter the text you want your avatar to speak...",
            height=150,
            help="Enter any text up to 200 characters for optimal speed"
        )
        
        # Character counter
        char_count = len(text_input)
        if char_count > 200:
            st.warning(f"⚠️ Text will be truncated to 200 characters for speed optimization (current: {char_count})")
        else:
            st.info(f"📝 Characters: {char_count}/200")
    
    # Generate button
    if uploaded_file and text_input.strip():
        if st.button("🚀 Generate Ultra-Fast Talking Avatar", type="primary", use_container_width=True):
            # Save uploaded image
            sadtalker_images_dir = os.path.join(os.path.dirname(__file__), "SadTalker", "examples", "source_image")
            os.makedirs(sadtalker_images_dir, exist_ok=True)
            
            image_path, filename = save_uploaded_image(uploaded_file, sadtalker_images_dir)
            
            if image_path:
                try:
                    # Setup progress UI
                    st.markdown("### 🚀 Ultra-Optimized Pipeline Progress")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    time_text = st.empty()
                    details_text = st.empty()
                    
                    progress_elements = {
                        'progress_bar': progress_bar,
                        'status_text': status_text,
                        'time_text': time_text,
                        'details_text': details_text
                    }
                    
                    # Generate avatar with progress tracking
                    with st.spinner("🔄 Generating ultra-fast talking avatar..."):
                        result = asyncio.run(generate_talking_avatar_ultra_fast(
                            image_path, text_input, progress_elements
                        ))
                    
                    # Display results
                    if result.get("success"):
                        st.markdown(f'''
                        <div class="success-box">
                            <h3>🎉 Ultra-Fast Generation Complete!</h3>
                            <p><strong>⏱️ Total Time:</strong> {result.get("total_time", 0):.2f} seconds</p>
                            <p><strong>� Audio Time:</strong> {result.get("audio_time", 0):.2f} seconds</p>
                            <p><strong>� Video Time:</strong> {result.get("video_time", 0):.2f} seconds</p>
                            <p><strong>🚀 Speedup:</strong> {result.get("speedup", 0):.1f}x faster than baseline</p>
                            <p><strong>🎯 Target Achieved:</strong> {"✅ YES" if result.get("target_achieved", False) else "❌ NO"}</p>
                            <p><strong>🔧 Backend:</strong> {result.get("backend", "Ultra-Optimized SadTalker")}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Display video
                        if result.get("video_path"):
                            video_full_path = os.path.join(os.path.dirname(__file__), result["video_path"])
                            
                            if os.path.exists(video_full_path):
                                st.subheader("🎬 Your Ultra-Fast Talking Avatar")
                                
                                # Video player
                                st.video(video_full_path)
                                
                                # Download button
                                with open(video_full_path, "rb") as video_file:
                                    video_bytes = video_file.read()
                                    st.download_button(
                                        label="📥 Download Video",
                                        data=video_bytes,
                                        file_name=f"ultra_fast_avatar_{int(time.time())}.mp4",
                                        mime="video/mp4"
                                    )
                                
                                # Video info
                                video_size = os.path.getsize(video_full_path)
                                st.info(f"📊 Video: {video_size:,} bytes ({video_size/1024/1024:.1f} MB)")
                                
                                # Performance metrics
                                st.subheader("📈 Performance Metrics")
                                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                                
                                with metric_col1:
                                    st.metric("⏱️ Total Time", f"{result.get('total_time', 0):.1f}s")
                                
                                with metric_col2:
                                    st.metric("🚀 Speedup", f"{result.get('speedup', 0):.1f}x")
                                
                                with metric_col3:
                                    st.metric("🎯 Target", "< 60s", 
                                             delta="✅ Achieved" if result.get('target_achieved', False) else "❌ Missed")
                                
                                with metric_col4:
                                    st.metric("💾 Video Size", f"{video_size/1024/1024:.1f} MB")
                            
                    else:
                        st.markdown(f'''
                        <div class="error-box">
                            <h3>❌ Ultra-Fast Generation Failed</h3>
                            <p>{result.get("error", "Unknown error occurred")}</p>
                            <p><strong>Time elapsed:</strong> {result.get("total_time", 0):.2f} seconds</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f'''
                    <div class="error-box">
                        <h3>❌ Error</h3>
                        <p>{str(e)}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                finally:
                    # Clean up uploaded image
                    try:
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)
                    except:
                        pass

    else:
        # Instructions
        st.markdown('''
        <div class="feature-box">
            <h3>🚀 Ultra-Fast Avatar Generation</h3>
            <p>1. Upload a clear photo with a visible face</p>
            <p>2. Enter the text you want your avatar to speak (up to 200 chars)</p>
            <p>3. Click "Generate Ultra-Fast Talking Avatar"</p>
            <p>4. Watch the real-time progress and get your video in under 60 seconds!</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Features
        st.subheader("⚡ Ultra-Optimization Features")
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            **🚀 Maximum Speed**
            - 128px resolution for speed
            - No enhancement processing
            - Aggressive optimizations
            """)
        
        with feature_col2:
            st.markdown("""
            **📊 Real-Time Progress**
            - Live progress bar
            - Step-by-step tracking
            - ETA estimation
            """)
        
        with feature_col3:
            st.markdown("""
            **⚡ Performance Target**
            - Sub-60 second generation
            - 100x+ speedup
            - Instant feedback
            """)

if __name__ == "__main__":
    # Add missing import
    import subprocess
    main()
