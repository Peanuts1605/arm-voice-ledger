#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EVIDENCE="$ROOT/demo/evidence"
OUTPUT="$ROOT/demo/arm-voice-ledger-evidence-walkthrough.mp4"
PYTHON_BIN="${VOICE_LEDGER_PYTHON:-$ROOT/.venv/bin/python}"
FONT="${VOICE_LEDGER_FONT:-/System/Library/Fonts/Supplemental/Arial Bold.ttf}"
FFMPEG_BIN="${FFMPEG_BIN:-$("$PYTHON_BIN" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')}"

for still in 01-source.png 02-evidence.png 03-replayable-ledger.png; do
  test -f "$EVIDENCE/$still" || {
    echo "Missing $EVIDENCE/$still. Run the browser proof first." >&2
    exit 1
  }
done

"$FFMPEG_BIN" -y \
  -loop 1 -t 5 -i "$EVIDENCE/01-source.png" \
  -loop 1 -t 5 -i "$EVIDENCE/02-evidence.png" \
  -loop 1 -t 5 -i "$EVIDENCE/03-replayable-ledger.png" \
  -filter_complex "\
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,drawtext=fontfile='$FONT':text='1. Choose a short local voice note':x=72:y=980:fontsize=38:fontcolor=0x183b3c:box=1:boxcolor=0xfbf7ed@0.94:boxborderw=18[v0]; \
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,drawtext=fontfile='$FONT':text='2. Turn timestamps into evidence':x=72:y=980:fontsize=38:fontcolor=0x183b3c:box=1:boxcolor=0xfbf7ed@0.94:boxborderw=18[v1]; \
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,drawtext=fontfile='$FONT':text='3. Replay the moment behind each decision':x=72:y=980:fontsize=38:fontcolor=0x183b3c:box=1:boxcolor=0xfbf7ed@0.94:boxborderw=18[v2]; \
    [v0][v1]xfade=transition=fade:duration=0.55:offset=4.45[v01]; \
    [v01][v2]xfade=transition=fade:duration=0.55:offset=8.9[out]" \
  -map "[out]" -t 13.35 -r 30 -pix_fmt yuv420p -movflags +faststart "$OUTPUT"

printf 'Evidence walkthrough: %s\n' "$OUTPUT"
