#!/usr/bin/env bash
set -euo pipefail

REPOROOT="$(cd "$(dirname "$0")" && pwd)"

if (($#)); then
  docker sandbox run claude "$REPOROOT" -- "$@"
else
  docker sandbox run claude "$REPOROOT"
fi