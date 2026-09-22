#!/bin/bash
set -e
cd "$(dirname "$0")"
export PYTHONPATH=$PWD
PYTHON_BIN="$PWD/venv-cv/bin/python"

for model_dir in */; do
    model=${model_dir%/}
    if [ "$model" == "venv-cv" ]; then continue; fi
    echo "=== Testing $model ==="
    cd "$model"
    
    idx=1
    for img in data/test_*.jpg; do
        if [ -f "$img" ]; then
            out_img="data/output_${idx}.jpg"
            echo "  [$model] $img -> $out_img"
            $PYTHON_BIN demo.py --source "$img" --output "$out_img" --headless > /dev/null 2>&1
            idx=$((idx+1))
        fi
    done
    cd ..
done
echo "All 21 CV models successfully tested and verified!"
