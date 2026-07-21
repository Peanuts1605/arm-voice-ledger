#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EVIDENCE="$ROOT/demo/evidence"
OUTPUT="$ROOT/demo/arm-voice-ledger-contest-demo.mp4"
PYTHON_BIN="${VOICE_LEDGER_PYTHON:-$ROOT/.venv/bin/python}"
FONT_DISPLAY="${VOICE_LEDGER_DISPLAY_FONT:-/System/Library/Fonts/Supplemental/Georgia Bold.ttf}"
FONT_UI="${VOICE_LEDGER_UI_FONT:-/System/Library/Fonts/Supplemental/Arial Bold.ttf}"
FFMPEG_BIN="${FFMPEG_BIN:-$("$PYTHON_BIN" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')}"

for still in 01-source.png 02-evidence.png 03-replayable-ledger.png; do
  test -f "$EVIDENCE/$still" || {
    echo "Missing $EVIDENCE/$still. Run the browser proof first." >&2
    exit 1
  }
done

# A compact companion cut: every product scene is captured from the real
# browser proof. The title and proof cards only state measured, local facts.
"$FFMPEG_BIN" -y \
  -f lavfi -t 4 -i "color=c=0xeaf0ed:s=1920x1080:r=30" \
  -loop 1 -t 6 -i "$EVIDENCE/01-source.png" \
  -loop 1 -t 6 -i "$EVIDENCE/02-evidence.png" \
  -loop 1 -t 6 -i "$EVIDENCE/03-replayable-ledger.png" \
  -f lavfi -t 5 -i "color=c=0x183b3c:s=1920x1080:r=30" \
  -filter_complex "\
    [0:v]drawtext=fontfile='$FONT_UI':text='LOCAL LISTENING DESK':x=120:y=142:fontsize=32:fontcolor=0x557b78,drawtext=fontfile='$FONT_DISPLAY':text='Arm Voice Ledger':x=120:y=242:fontsize=92:fontcolor=0x183b3c,drawtext=fontfile='$FONT_DISPLAY':text='A voice note becomes a decision only when':x=120:y=390:fontsize=52:fontcolor=0x183b3c,drawtext=fontfile='$FONT_DISPLAY':text='you can point back to the moment that earned it.':x=120:y=458:fontsize=52:fontcolor=0x183b3c,drawtext=fontfile='$FONT_UI':text='MLX Whisper on Apple silicon  •  local timestamped evidence  •  human-owned ledger':x=120:y=810:fontsize=26:fontcolor=0x466765,drawbox=x=120:y=900:w=438:h=72:color=0xf0cf84@1:t=fill,drawtext=fontfile='$FONT_UI':text='ARM CREATE\\: MOBILE AI':x=150:y=922:fontsize=27:fontcolor=0x183b3c[intro]; \
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,fps=30,drawbox=x=0:y=890:w=1920:h=190:color=0xfbf7ed@0.96:t=fill,drawtext=fontfile='$FONT_UI':text='01  SOURCE':x=84:y=928:fontsize=27:fontcolor=0x557b78,drawtext=fontfile='$FONT_DISPLAY':text='Choose one short local voice note.':x=84:y=978:fontsize=47:fontcolor=0x183b3c,drawtext=fontfile='$FONT_UI':text='The request file is removed after local transcription.':x=84:y=1033:fontsize=26:fontcolor=0x466765[source]; \
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,fps=30,drawbox=x=0:y=890:w=1920:h=190:color=0xfbf7ed@0.96:t=fill,drawtext=fontfile='$FONT_UI':text='02  EVIDENCE':x=84:y=928:fontsize=27:fontcolor=0x557b78,drawtext=fontfile='$FONT_DISPLAY':text='Keep timestamps attached to what was said.':x=84:y=978:fontsize=47:fontcolor=0x183b3c,drawtext=fontfile='$FONT_UI':text='The synthetic proof returned 16 timestamped words offline.':x=84:y=1033:fontsize=26:fontcolor=0x466765[evidence]; \
    [3:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xeaf0ed,setsar=1,fps=30,drawbox=x=0:y=890:w=1920:h=190:color=0xfbf7ed@0.96:t=fill,drawtext=fontfile='$FONT_UI':text='03  DECISION LEDGER':x=84:y=928:fontsize=27:fontcolor=0x557b78,drawtext=fontfile='$FONT_DISPLAY':text='Save only what matters, then replay the proof.':x=84:y=978:fontsize=47:fontcolor=0x183b3c,drawtext=fontfile='$FONT_UI':text='Every row stays editable and points to its local source moment.':x=84:y=1033:fontsize=26:fontcolor=0x466765[ledger]; \
    [4:v]drawtext=fontfile='$FONT_UI':text='ARM VOICE LEDGER':x=120:y=210:fontsize=34:fontcolor=0xb8d1cd,drawtext=fontfile='$FONT_DISPLAY':text='Source -> timestamp -> decision -> replay':x=120:y=354:fontsize=62:fontcolor=0xfbf7ed,drawtext=fontfile='$FONT_UI':text='A compact, reproducible Apple-silicon proof.':x=120:y=456:fontsize=32:fontcolor=0xb8d1cd,drawbox=x=120:y=692:w=860:h=96:color=0xf0cf84@1:t=fill,drawtext=fontfile='$FONT_UI':text='PUBLIC MIT SOURCE  •  LOCAL SMOKE RUN':x=158:y=728:fontsize=25:fontcolor=0x183b3c[outro]; \
    [intro][source]xfade=transition=fade:duration=0.6:offset=3.4[v01]; \
    [v01][evidence]xfade=transition=fade:duration=0.6:offset=8.8[v02]; \
    [v02][ledger]xfade=transition=fade:duration=0.6:offset=14.2[v03]; \
    [v03][outro]xfade=transition=fade:duration=0.6:offset=19.6[out]" \
  -map "[out]" -t 24.4 -r 30 -pix_fmt yuv420p -movflags +faststart "$OUTPUT"

printf 'Contest demo: %s\n' "$OUTPUT"
