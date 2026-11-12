#!/usr/bin/env bash
# Build Arcana RPG into .mcpack / .mcaddon
set -euo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"

OUT=dist
rm -rf "$OUT"
mkdir -p "$OUT"

# regenerate everything from source-of-truth scripts
python3 tools/gen_textures.py
python3 tools/gen_pack.py

# .mcpack = a zip whose ROOT contains manifest.json
( cd src/ArcanaBP && zip -qr -X ../../"$OUT"/ArcanaRPG_BP.mcpack . -x '.*' )
( cd src/ArcanaRP && zip -qr -X ../../"$OUT"/ArcanaRPG_RP.mcpack . -x '.*' )

# .mcaddon = one zip containing both packs as folders
rm -rf /tmp/mcaddon && mkdir -p /tmp/mcaddon
cp -r src/ArcanaBP /tmp/mcaddon/ArcanaRPG_BP
cp -r src/ArcanaRP /tmp/mcaddon/ArcanaRPG_RP
( cd /tmp/mcaddon && zip -qr -X "$OLDPWD/$OUT/ArcanaRPG.mcaddon" . -x '.*' )

echo "--- built ---"
ls -lh "$OUT"
