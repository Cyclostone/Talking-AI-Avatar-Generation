# AI Avatar Pipeline - Clean Codebase

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