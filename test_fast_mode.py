#!/usr/bin/env python3
"""
Quick Test: Fast Mode Optimization
Test the fastest SadTalker optimization mode for Daylily challenge
"""

import asyncio
import sys
import os
import time

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_fast_mode():
    """Test fast mode optimization"""
    print("⚡ Testing FAST Mode SadTalker Optimization")
    print("🎯 Goal: Maximum speed while maintaining decent quality")
    print("="*60)
    
    test_text = "Testing fast mode optimization for Daylily challenge."
    baseline_time = 959.0  # From previous GPU test
    
    print(f"📝 Test text: '{test_text}'")
    print(f"⏱️ Baseline: {baseline_time}s (16 minutes)")
    print(f"🎯 Target: <60s (significant improvement)")
    print(f"🏆 Dream target: <2s (Daylily challenge)")
    
    try:
        from optimized_sadtalker_pipeline import OptimizedSadTalkerPipeline
        
        # Test FAST mode (maximum speed optimization)
        print(f"\n⚡ Initializing FAST mode pipeline...")
        pipeline = OptimizedSadTalkerPipeline(quality_mode="fast")
        
        start_time = time.time()
        result = await pipeline.generate_avatar_video(test_text)
        total_time = time.time() - start_time
        
        if result["success"]:
            speedup = baseline_time / result['total_time']
            
            print(f"\n✅ FAST MODE RESULTS:")
            print(f"   ⏱️ Time: {result['total_time']:.1f}s")
            print(f"   🚀 Speedup: {speedup:.1f}x faster than baseline")
            print(f"   🏆 Quality: {result['quality']}")
            print(f"   🎯 Status: {result['daylily_status']}")
            
            # Assessment
            if result['total_time'] < 2.0:
                print(f"\n🏆 AMAZING! Daylily challenge ACHIEVED!")
                print(f"   Ready for Phase 3: Serverless deployment")
            elif result['total_time'] < 60.0:
                print(f"\n🎯 EXCELLENT! Significant speedup achieved")
                print(f"   Continue with further optimizations")
            elif result['total_time'] < 300.0:  # <5 minutes
                print(f"\n👍 GOOD! Meaningful improvement")
                print(f"   Try more aggressive optimizations")
            else:
                print(f"\n⏱️ PARTIAL: Some improvement, needs more work")
            
            # Quality check
            if result.get('video_path'):
                project_root = os.path.dirname(os.path.abspath(__file__))
                video_full_path = os.path.join(project_root, result['video_path'])
                if os.path.exists(video_full_path):
                    video_size = os.path.getsize(video_full_path)
                    print(f"\n📊 Quality verification:")
                    print(f"   Video size: {video_size:,} bytes")
                    if video_size > 100000:  # >100KB
                        print(f"   ✅ Good quality maintained")
                    else:
                        print(f"   ⚠️ Quality may be reduced")
            
            return True, result['total_time'], result['quality']
            
        else:
            print(f"\n❌ FAST mode failed: {result.get('error', 'Unknown error')}")
            return False, 0.0, 'ERROR'
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure optimized_sadtalker_pipeline.py exists in app/ directory")
        return False, 0.0, 'ERROR'
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False, 0.0, 'ERROR'

if __name__ == "__main__":
    print("⚡ Starting Fast Mode Optimization Test")
    print("Phase 2 of Daylily AI Avatar Challenge")
    
    try:
        success, time_taken, quality = asyncio.run(test_fast_mode())
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        if success:
            print(f"✅ Fast mode optimization: WORKING")
            print(f"   - Time: {time_taken:.1f}s")
            print(f"   - Quality: {quality}")
            
            if time_taken < 2.0:
                print("🏆 DAYLILY CHALLENGE ACHIEVED!")
                print("💡 Next: Serverless deployment preparation")
            elif time_taken < 60.0:
                print("🎯 Significant improvement achieved!")
                print("💡 Next: Try balanced mode or further optimizations")
            else:
                print("⏱️ Some improvement, continue optimizing")
                print("💡 Next: Try alternative optimization approaches")
        else:
            print("❌ Fast mode optimization needs debugging")
            print("💡 Check SadTalker parameters and GPU setup")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
