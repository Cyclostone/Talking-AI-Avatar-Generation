import argparse
import os
from gtts import gTTS
from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser(description='Generate audio using Google TTS')
    parser.add_argument('--text', required=True, help='Text to convert to speech')
    parser.add_argument('--output', required=True, help='Output audio file path')
    
    args = parser.parse_args()
    
    # Debug print to verify text is received correctly
    print(f"DEBUG: Received text: '{args.text}'")
    print(f"DEBUG: Output path: '{args.output}'")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Generate audio using gTTS (outputs MP3)
    print(f"Generating audio for text: '{args.text}'")
    tts = gTTS(text=args.text, lang='en', slow=False)
    
    # Save as temporary MP3 file first
    temp_mp3 = args.output.replace('.wav', '_temp.mp3')
    tts.save(temp_mp3)
    
    # Convert MP3 to WAV if output is WAV format
    if args.output.endswith('.wav'):
        print("Converting MP3 to WAV format...")
        audio = AudioSegment.from_mp3(temp_mp3)
        audio.export(args.output, format="wav")
        os.remove(temp_mp3)  # Clean up temp file
    else:
        # Just rename the MP3 file
        os.rename(temp_mp3, args.output)
    
    print(f"Audio generated: {args.output}")

if __name__ == "__main__":
    main()
