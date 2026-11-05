#!/bin/bash
# Rebuild and take every deliverable, in order (run from anywhere).
set -e
cd "$(dirname "$0")"
U="uv run -q --with playwright python -I"
P="uv run -q --with playwright --with pillow python -I"
uv run -q --with fonttools --with brotli python -I marks.py
python3 build.py
timeout 200 $U sheetshot.py
timeout 120 $U shot.py ../hero-1440.png 1440 900 dark 3600
timeout 120 $U shot.py ../hero-1440-light.png 1440 900 light 3600
timeout 400 $U sections.py .. 1440 dark
timeout 300 $U fullpage.py ../full-1440.png 1440 dark
timeout 300 $U fullpage.py ../phone-390.png 390 dark
timeout 300 $U fullpage.py ../phone-320.png 320 dark
timeout 120 $P frames.py
timeout 180 $P crops.py
uv run -q --with pillow python -I trim.py
echo FINAL-DONE
