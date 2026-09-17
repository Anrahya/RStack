#!/usr/bin/env bash
# Copy this plugin into Cursor's local plugin folder.
# Cursor skips symlinks that point outside ~/.cursor/plugins/local.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${HOME}/.cursor/plugins/local/r-stack"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"
# Copy contents, not a symlink to ~/plugins.
cp -a "$ROOT"/. "$DEST/"
echo "Installed R-Stack Cursor plugin to $DEST"
echo "Reload the Cursor window (Developer: Reload Window) to pick it up."
