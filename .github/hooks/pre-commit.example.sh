#!/usr/bin/env bash
set -euo pipefail

status=0
while IFS= read -r -d '' file; do
  [[ -f "$file" ]] || continue
  if grep -nE '\[(CITATION NEEDED|TODO: cite)\]' "$file"; then
    printf 'Unresolved citation marker in staged file: %s\n' "$file" >&2
    status=1
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z -- '*.md' '*.bib')

if (( status != 0 )); then
  printf 'Resolve citation markers before committing.\n' >&2
  exit 1
fi
