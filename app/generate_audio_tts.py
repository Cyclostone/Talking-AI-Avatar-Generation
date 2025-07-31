import argparse
import os
from TTS.api import TTS

def main():
    parser = argparse.ArgumentParser(description='Generate audio using Coqui TTS')
    parser.add_argument('--text', required=True, help='Text to convert to speech')
    parser.add_argument('--output', required=True, help='Output audio file path')
    
    args = parser.parse_args()
    
    # Debug print to verify text is received correctly
    print(f"DEBUG: Received text: '{args.text}'")
    print(f"DEBUG: Output path: '{args.output}'")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Initialize TTS
    print("Initializing TTS model...")
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    
    # Generate audio
    print(f"Generating audio for text: '{args.text}'")
    tts.tts_to_file(text=args.text, file_path=args.output)
    
    print(f"Audio generated: {args.output}")

if __name__ == "__main__":
    main()
