#!/usr/bin/env bash
# Render the BridgeSplat scenes at 1080p30 and copy them to ../slides/assets/.
#   ./render.sh                      all scenes
#   ./render.sh S3_MonoRay           one scene
# Setup (once): brew install cairo pkgconf
#               uv sync           (from the repo root; env lives in <root>/.venv)
set -euo pipefail
cd "$(dirname "$0")"

out_name() {
  case "$1" in
    S1_ConstrainedParams) echo bridgesplat-1-what-is-learned ;;
    S2_GradientFlow)      echo bridgesplat-2-gradient-flow ;;
    S3_MonoRay)           echo bridgesplat-3-mono-ray ;;
    S4_MonoTracking)      echo bridgesplat-4-mono-tracking ;;
    *) echo "unknown scene $1" >&2; exit 1 ;;
  esac
}

uv run python toy_splat2d.py   # builds cache/toy.npz once and prints the numbers shown in S3/S4

if [ $# -eq 0 ]; then set -- S1_ConstrainedParams S2_GradientFlow S3_MonoRay S4_MonoTracking; fi
for s in "$@"; do
  name=$(out_name "$s")
  uv run manim -r 1920,1080 --fps 30 bridgesplat_scenes.py "$s"
  cp "media/videos/bridgesplat_scenes/1080p30/$s.mp4" "../slides/assets/$name.mp4"
  echo "-> slides/assets/$name.mp4"
done
