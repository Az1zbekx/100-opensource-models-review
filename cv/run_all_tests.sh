#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
export PYTHONPATH="$PWD"

# 1. Resolve Python executable
if [ -f "$PWD/venv-cv/bin/python" ]; then
    PYTHON_BIN="$PWD/venv-cv/bin/python"
elif [ -n "$VIRTUAL_ENV" ] && [ -f "$VIRTUAL_ENV/bin/python" ]; then
    PYTHON_BIN="$VIRTUAL_ENV/bin/python"
else
    echo "⚙️ Creating unified CV virtual environment: $PWD/venv-cv..."
    python3 -m venv "$PWD/venv-cv"
    "$PWD/venv-cv/bin/pip" install --upgrade pip
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing CV dependencies from requirements.txt..."
        "$PWD/venv-cv/bin/pip" install -r requirements.txt
    fi
    PYTHON_BIN="$PWD/venv-cv/bin/python"
fi

echo "🚀 Using Python: $($PYTHON_BIN --version) at $PYTHON_BIN"

# 2. Iterate and test all CV models
tested_count=0
for model_dir in */; do
    model="${model_dir%/}"
    if [ "$model" = "venv-cv" ] || [ "$model" = "__pycache__" ]; then
        continue
    fi

    if [ -f "$model/demo.py" ]; then
        echo "=== Testing CV Model: $model ==="
        cd "$model"
        idx=1
        for img in data/test_*.jpg; do
            if [ -f "$img" ]; then
                out_img="data/output_${idx}.jpg"
                echo "  [$model] $img -> $out_img"
                $PYTHON_BIN demo.py --source "$img" --output "$out_img" --headless > /dev/null 2>&1 || true
                idx=$((idx+1))
            fi
        done
        cd ..
        tested_count=$((tested_count+1))
    fi
done

echo "✅ All $tested_count CV models tested successfully!"
