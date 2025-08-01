#!/usr/bin/env python3
"""
Simple GPU Pipeline Test
Quick test of GPU-accelerated SadTalker pipeline for Daylily challenge
"""

import asyncio
import sys
import os
import time

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_gpu_acceleration():
    """Test GPU-accelerated pipeline"""
    print("🚀 Testing GPU-Accelerated SadTalker Pipeline")
    print("🎯 Goal: Beat baseline 852s (14.2min) while maintaining quality")
    print("="*60)
    
    try:
        from gpu_accelerated_pipeline import GPUAcceleratedAvatarPipeline
        
        # Test text
        test_text = "Testing GPU acceleration for faster avatar generation."
        
        print(f"📝 Test text: '{test_text}'")
        print(f"⏱️ Baseline time: 852 seconds (14.2 minutes)")
        print(f"🎯 Target: <2 seconds (Daylily challenge)")
        
        # Initialize pipeline
        pipeline = GPUAcceleratedAvatarPipeline(enable_gpu=True)
        
        # Run test
        start_time = time.time()
        result = await pipeline.generate_avatar_video(test_text)
        total_time = time.time() - start_time
        
        # Results
        if result["success"]:
            print(f"\n✅ SUCCESS!")
            print(f"⏱️ GPU time: {result['total_time']:.1f}s")
            print(f"🚀 Speedup: {852/result['total_time']:.1f}x faster than baseline")
            print(f"🏆 Quality: {result['quality']}")
            print(f"🎯 Daylily status: {result['daylily_status']}")
            
            if result['total_time'] < 2.0:
                print("🏆 DAYLILY CHALLENGE ACHIEVED!")
            elif result['total_time'] < 60.0:
                print("🎯 Significant improvement - continue optimizing")
            else:
                print("⏱️ Needs more optimization")
                
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure gpu_accelerated_pipeline.py exists in app/ directory")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_gpu_acceleration())
