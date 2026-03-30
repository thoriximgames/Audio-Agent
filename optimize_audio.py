import os
import subprocess
import re

# Configuration
SFX_THRESHOLD = 500  # OGG is fine under 500KB
MUSIC_THRESHOLD = 1000 # Music should be MP3
DEFAULT_ARTIST = "Audio Agent"
DEFAULT_ALBUM = "Project Assets"

def clean_filename(filename):
    """
    Standardize filename: lowercase, snake_case, remove special characters.
    """
    name, ext = os.path.splitext(filename)
    # Remove special characters and replace spaces/hyphens with underscores
    name = re.sub(r'[^a-zA-Z0-0\s_-]', '', name)
    name = re.sub(r'[\s-]+', '_', name).strip('_').lower()
    return f"{name}{ext}"

def run_ffmpeg(input_file, output_file, title):
    """
    Run FFmpeg to convert format, normalize sample rate, and update metadata.
    """
    try:
        # Standardize: 44.1kHz, Strip all metadata, Add custom metadata
        cmd = [
            "ffmpeg", "-i", input_file, 
            "-ar", "44100", 
            "-map_metadata", "-1", 
            "-metadata", f"title={title}",
            "-metadata", f"artist={DEFAULT_ARTIST}",
            "-metadata", f"album={DEFAULT_ALBUM}",
            "-metadata", "comment=Processed by Audio Agent",
            "-y", output_file
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to process {input_file}: {e}")
        return False

def process_audio_library(root_dir):
    print(f"--- Audio Agent: Processing {os.path.abspath(root_dir)} ---")
    
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            size_kb = os.path.getsize(file_path) / 1024
            ext = file.lower().split('.')[-1]
            
            if ext not in ["mp3", "ogg", "wav", "flac"]:
                continue

            # 1. Determine New Name (Cleaned)
            new_file_name = clean_filename(file)
            base_name_clean = os.path.splitext(new_file_name)[0]
            
            # 2. Determine Target Format
            target_ext = "ogg" # Default for SFX
            if any(k in file.lower() for k in ["music", "ambience", "bgm", "track"]) or size_kb > MUSIC_THRESHOLD:
                target_ext = "mp3"
            
            target_name = f"{base_name_clean}.{target_ext}"
            target_path = os.path.join(subdir, target_name)
            
            # 3. Process if needed (Format change, Name change, or just to update metadata)
            # We always process to ensure metadata and sample rate are correct.
            temp_path = os.path.join(subdir, f"temp_{target_name}")
            
            title = base_name_clean.replace('_', ' ').title()
            
            print(f"Processing: {file}")
            print(f"  -> Clean Name: {target_name}")
            print(f"  -> Format:     {target_ext.upper()}")
            print(f"  -> Title:      {title}")

            if run_ffmpeg(file_path, temp_path, title):
                # Remove original if it's different from target or if we just want to replace it
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # If target already exists (e.g. from a previous run or same name), remove it
                if os.path.exists(target_path):
                    os.remove(target_path)
                    
                os.rename(temp_path, target_path)
                print(f"  [SUCCESS] Created {target_name}")
            else:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

if __name__ == "__main__":
    # Check for ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Error: FFmpeg not found. Please install it with: winget install -e --id Gyan.FFmpeg")
        exit(1)

    # Process Audio folder primarily
    audio_dir = "Audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        
    process_audio_library(audio_dir)
    print("\n--- Audio Agent: Work Complete ---")
