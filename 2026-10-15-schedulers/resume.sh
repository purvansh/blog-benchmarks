#!/usr/bin/env bash
# Timers are stopped. Stay down long enough to miss several minutely fires,
# then bring both back and record which one makes up the missed run.
cd "$(dirname "$0")"
echo "=== down from $(date -Iseconds) ===" >> fires.log
sleep 210
echo "=== restarting at $(date -Iseconds) ===" >> fires.log
systemctl --user start blogtest-persistent.timer blogtest-volatile.timer
sleep 20
echo "=== 20s after restart, before the next scheduled fire ===" >> fires.log
cat fires.log
