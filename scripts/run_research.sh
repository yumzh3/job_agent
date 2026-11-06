#!/bin/bash
# Research agent: one run per role, adding only new interview-prep notes.
# Run by launchd weekly (see launchd/), or by hand: bash scripts/run_research.sh

cd "$(dirname "$0")/.." || exit 1
PY=".venv/bin/python"
mkdir -p data/logs
LOG="data/logs/research.log"

ROLES=("data scientist" "applied scientist")      # edit to change which roles are researched

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

for i in $(seq 1 20); do
    curl -s --max-time 5 https://api.anthropic.com > /dev/null && break
    log "Waiting for network ($i/20)..."
    sleep 30
done

log "=== Research start ==="
for ROLE in "${ROLES[@]}"; do
    log "Role: $ROLE"
    $PY agent.py "$ROLE" >> "$LOG" 2>&1 || log "agent.py failed for '$ROLE'"
done
log "=== Research end ==="

osascript -e "display notification \"Research notes updated for: ${ROLES[*]}\" with title \"Interview research\"" 2>/dev/null
