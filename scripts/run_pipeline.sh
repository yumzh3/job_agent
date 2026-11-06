#!/bin/bash
# Job pipeline: fetch new postings, score them, write the digest.
# Run by launchd on a schedule (see launchd/), or by hand: bash scripts/run_pipeline.sh

cd "$(dirname "$0")/.." || exit 1          # project folder, wherever this script lives
caffeinate -i -w $$ &                      # keep the Mac awake until this script finishes
PY=".venv/bin/python -u"
mkdir -p data/logs
LOG="data/logs/pipeline.log"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

# After waking from sleep, the network can take a minute; wait up to 10 minutes.
for i in $(seq 1 20); do
    curl -s --max-time 5 https://api.anthropic.com > /dev/null && break
    log "Waiting for network ($i/20)..."
    sleep 30
done

log "=== Pipeline start ==="
$PY fetch_jobs.py  >> "$LOG" 2>&1 || log "fetch_jobs.py failed (continuing with jobs already saved)"
$PY score_jobs.py  >> "$LOG" 2>&1 || log "score_jobs.py failed (unscored jobs will be retried next run)"
SUMMARY=$($PY digest.py --min-score 5 2>&1) || log "digest.py failed"
log "$SUMMARY"
log "=== Pipeline end ==="

# A macOS notification so you know a digest is ready.
osascript -e "display notification \"$SUMMARY\" with title \"Job digest\"" 2>/dev/null
