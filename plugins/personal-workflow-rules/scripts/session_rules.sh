#!/bin/sh
# SessionStart: inject rules.md into context, and install pstack-models.md
# into ~/.claude/rules/ when missing (pstack skills read that path).
# An existing local file wins; this never overwrites it.
here="$(dirname "$0")/.."
dest="$HOME/.claude/rules/pstack-models.md"
if [ ! -f "$dest" ]; then
  mkdir -p "$HOME/.claude/rules" && cp "$here/pstack-models.md" "$dest"
fi
cat "$here/rules.md"
