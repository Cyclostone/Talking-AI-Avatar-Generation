#!/usr/bin/env python3
"""
Codebase Cleanup Script
Removes unnecessary test and experimental files, keeps only essential working components
"""

import os
import shutil
import sys

def cleanup_codebase():
    """Clean up the AI Avatar project codebase"""
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"🧹 Cleaning up codebase in: {project_root}")
    
    # Files to remove (unnecessary/experimental)
    files_to_remove = [
        # Test files
        "test_api_audio.py",
        "test_hybrid.py", 
        "test_improved.py",
        "test_optimization.py",
        "quick_test.py",
        "debug_audio.py",
        
        # Experimental app files
        "app/test_gtts.py",
        "app/test_tts.py",
        "app/verify_audio.py",
        "app/generate_audio_not_working.py",
        "app/generate_audio_tts.py",  # Keep only gtts version
        
        # Experimental pipeline files
        "app/optimized_pipeline.py",
        "app/hybrid_optimized_pipeline.py", 
        "app/lightweight_animator.py",
        
        # Experimental server files
        "server/optimized_app.py",
        "server/hybrid_app.py",
        
        # Experimental requirements
        "requirements-optimized.txt",
    ]
    
    # Directories to clean (remove contents but keep structure)
    dirs_to_clean = [
        "app/__pycache__",
        "server/__pycache__",
    ]
    
    removed_count = 0
    
    print("\n🗑️ Removing unnecessary files:")
    for file_path in files_to_remove:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                print(f"   ✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
        else:
            print(f"   ⚠️ Not found: {file_path}")
    
    print("\n🧹 Cleaning cache directories:")
    for dir_path in dirs_to_clean:
        full_path = os.path.join(project_root, dir_path)
        if os.path.exists(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"   ✅ Cleaned: {dir_path}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to clean {dir_path}: {e}")
    
    print(f"\n✅ Cleanup completed! Removed {removed_count} items")
    
    # Show what's left (essential components)
    print("\n📋 Essential components remaining:")
    essential_files = [
        "app/improved_pipeline.py",      # Working baseline pipeline
        "app/run_pipeline.py",           # Original working pipeline (backup)
        "app/generate_audio_gtts.py",    # Working TTS audio generation
        "server/app.py",                 # Simple working API server
        "requirements-py311.txt",        # Working dependencies
        "README.md",                     # Documentation
    ]
    
    for file_path in essential_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"   ✅ {file_path} ({file_size:,} bytes)")
        else:
            print(f"   ❌ MISSING: {file_path}")
    
    print(f"\n🎯 Codebase is now clean and focused!")
    print(f"   - Removed experimental/test files")
    print(f"   - Kept only working components")
    print(f"   - Ready for production use")
    
    # Create a simple usage guide
    usage_guide = """# AI Avatar Pipeline - Clean Codebase

## Essential Components:
- `app/improved_pipeline.py` - Main working pipeline (async, reliable)
- `app/run_pipeline.py` - Original pipeline (backup reference)
- `app/generate_audio_gtts.py` - Audio generation using gTTS
- `server/app.py` - FastAPI server
- `requirements-py311.txt` - Python 3.11 dependencies

## Quick Start:
1. Activate environment: `conda activate avatar-dev-py311`
2. Test pipeline: `python -c "import asyncio; from app.improved_pipeline import generate_talking_avatar_improved; asyncio.run(generate_talking_avatar_improved('Hello world'))"`
3. Start server: `cd server && python app.py`

## Next Steps:
- Use improved_pipeline.py as production baseline
- Apply further optimizations gradually
- Always test against this working foundation
"""
    
    with open(os.path.join(project_root, "USAGE.md"), "w") as f:
        f.write(usage_guide.strip())
    
    print(f"📝 Created USAGE.md with quick start guide")

if __name__ == "__main__":
    try:
        cleanup_codebase()
        print(f"\n🎉 Cleanup successful!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        sys.exit(1)
