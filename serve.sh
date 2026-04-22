#!/usr/bin/env bash
set -e

PORT=${1:-3000}

echo "Serving at http://localhost:$PORT/clusterintro/"
uv run python -m http.server "$PORT"
