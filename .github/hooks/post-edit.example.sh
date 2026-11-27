#!/usr/bin/env bash
set -euo pipefail

if (( $# == 0 )); then
  printf 'Usage: %s FILE [FILE ...]\n' "$0" >&2
  exit 2
fi

status=0
for file in "$@"; do
  [[ -f "$file" ]] || {
    printf 'Edited file not found: %s\n' "$file" >&2
    status=1
    continue
  }
  case "$file" in
    *.md|*.bib)
      if grep -nE '\[(CITATION NEEDED|TODO: cite)\]' "$file"; then
        printf 'Unresolved citation marker in edited file: %s\n' "$file" >&2
        status=1
      fi
      ;;
  esac
done

exit "$status"
