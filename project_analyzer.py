import os

# Standards established by Audio Agent
STANDARDS = {
    "audio": {
        "sfx_format": ".ogg",
        "music_format": ".mp3",
        "music_keywords": ["music", "ambience", "bgm", "track"],
        "music_threshold_kb": 1000,
        "sample_rate": 44100,
        "loudness_lufs": -16.0,
        "valid_input_exts": [".wav", ".ogg", ".mp3", ".flac"]
    },
    "naming": {
        "disallowed_pattern": r'[^a-z0-9._]', # We prefer snake_case lowercase
        "required_style": "lowercase_snake_case"
    }
}

def analyze_audio_assets(root_dir):
    report = []
    
    for subdir, _, files in os.walk(root_dir):
        if ".git" in subdir or "temp_" in subdir:
            continue

        for file in files:
            file_path = os.path.join(subdir, file)
            size_kb = os.path.getsize(file_path) / 1024
            ext = os.path.splitext(file)[1].lower()
            name_lower = file.lower()

            if ext not in STANDARDS["audio"]["valid_input_exts"]:
                continue

            # Check Naming
            if any(c.isupper() for c in file) or ' ' in file or '-' in file:
                 report.append(f"[NAME]    {file}: Should be lowercase snake_case.")

            # Check Format logic
            is_music = any(k in name_lower for k in STANDARDS["audio"]["music_keywords"]) or size_kb > STANDARDS["audio"]["music_threshold_kb"]
            
            if is_music:
                if ext != STANDARDS["audio"]["music_format"]:
                    report.append(f"[FORMAT]  {file}: Music candidate should be {STANDARDS['audio']['music_format']} (found {ext}).")
            else:
                if ext != STANDARDS["audio"]["sfx_format"]:
                    report.append(f"[FORMAT]  {file}: SFX candidate should be {STANDARDS['audio']['sfx_format']} (found {ext}).")

    return report

if __name__ == "__main__":
    target = "Audio" # Analyze Audio folder
    print(f"--- Audio Project Health Check for: {os.path.abspath(target)} ---\n")
    
    findings = analyze_audio_assets(target)
    
    if not findings:
        print("Success: All audio assets follow project standards!")
    else:
        print(f"Found {len(findings)} issues to address:\n")
        for finding in sorted(findings):
            print(finding)
    
    print("\n--- End of Report ---")
