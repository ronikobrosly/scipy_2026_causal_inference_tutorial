#!/usr/bin/env bash
# Test a fresh install path in a throwaway Ubuntu container.
# Usage: ./test-install.sh <uv|pixi|make>
# Each run starts from a clean OS (no tooling, no caches, no .venv/.pixi).
set -euo pipefail

PATH_KIND="${1:?usage: test-install.sh <uv|pixi|make>}"
REPO="https://github.com/ronikobrosly/scipy_2026_causal_inference_tutorial.git"
IMAGE="ubuntu:24.04"

# Import check that all three paths share.
SMOKE='python -c "import dowhy, tensorflow, marimo, sklearn, pandas; print(\"SMOKE OK\")"'

case "$PATH_KIND" in
  uv)
    SCRIPT='
      set -euxo pipefail
      apt-get update -qq
      apt-get install -y -qq curl git graphviz graphviz-dev build-essential
      curl -LsSf https://astral.sh/uv/install.sh | sh
      export PATH="$HOME/.local/bin:$PATH"
      git clone --depth 1 '"$REPO"' repo
      cd repo
      uv sync
      uv run '"$SMOKE"'
    '
    ;;
  pixi)
    SCRIPT='
      set -euxo pipefail
      apt-get update -qq
      apt-get install -y -qq curl git
      curl -fsSL https://pixi.sh/install.sh | bash
      export PATH="$HOME/.pixi/bin:$PATH"
      git clone --depth 1 '"$REPO"' repo
      cd repo
      pixi install
      pixi run '"$SMOKE"'
    '
    ;;
  make)
    SCRIPT='
      set -euxo pipefail
      apt-get update -qq
      apt-get install -y -qq curl git make graphviz graphviz-dev build-essential
      curl -LsSf https://astral.sh/uv/install.sh | sh
      export PATH="$HOME/.local/bin:$PATH"
      curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
      apt-get install -y -qq nodejs
      git clone --depth 1 '"$REPO"' repo
      cd repo
      make setup            # = uv sync  +  npm install in the slides dir
      make check-deps
      uv run '"$SMOKE"'
    '
    ;;
  *)
    echo "unknown path: $PATH_KIND (use uv|pixi|make)" >&2; exit 2 ;;
esac

echo ">>> Testing '$PATH_KIND' path in a fresh $IMAGE container..."
docker run --rm "$IMAGE" bash -c "$SCRIPT"
echo ">>> '$PATH_KIND' path: PASSED"
