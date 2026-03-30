# Audio Agent Environment: Standards & Mandates

This environment is designed for the automated processing, normalization, and optimization of audio assets. All agents operating in this workspace MUST adhere to the following mandates.

## 1. Core Mandates
- **Tooling:** `ffmpeg` and `ffprobe` are required for all audio operations. Verify their availability before execution.
- **Source Integrity:** Never modify files in-place without a verified successful conversion. Always use temporary files during processing.
- **Standards Precedence:** The logic defined in `optimize_audio.py` is the source of truth for file processing.

## 2. Audio Standards
- **Sample Rate:** All processed audio MUST be normalized to **44100 Hz**.
- **Metadata:** All assets must have clean metadata. Custom tags (Title, Artist: "Audio Agent", Album: "Project Assets") are mandatory.
- **File Formats:**
    - **SFX:** Use `.ogg` (Vorbis) for sound effects and short clips (generally < 1000KB).
    - **Music/Ambience:** Use `.mp3` for long tracks, background music, or files > 1000KB.
    - **Naming:** All filenames MUST be `lowercase_snake_case`. No spaces, parentheses, or special characters are permitted.

## 3. Standard Workflows

### Processing Assets
To ingest and optimize new audio files:
1. Place raw assets in the `Audio/` directory.
2. Execute `python optimize_audio.py`.
3. Verify output via `ffprobe` to ensure metadata and sample rates are correct.

### Health Check & Validation
To verify the integrity of the audio library:
1. Execute `python project_analyzer.py`.
2. This script checks for naming violations, format mismatches (e.g., music stored as ogg), and unsupported extensions.

## 4. Troubleshooting
- If `ffmpeg` is missing, install it via: `winget install -e --id Gyan.FFmpeg`.
- If naming collisions occur, the `optimize_audio.py` script will overwrite the older target file with the newly processed version.
