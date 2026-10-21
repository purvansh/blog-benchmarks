# Which scheduler remembers a missed window

Two systemd user timers differing in one line, `Persistent=true` against
`Persistent=false`, both firing every minute. Stop both long enough to miss
four fires, start them together, read the log.

## Run

Install the two units (see `runner.sh` for the service payload), then:

```bash
systemctl --user start blogtest-persistent.timer blogtest-volatile.timer
# let them fire once
systemctl --user stop blogtest-persistent.timer blogtest-volatile.timer
./resume.sh      # stays down 210s, restarts both, prints the fire log
```

## Result

```
15:49:00 fired persistent
15:49:00 fired volatile
=== down from 15:49:56 ===
=== restarting at 15:53:26 ===
15:53:26 fired persistent        <-- catch-up, 34s before the next scheduled fire
15:54:00 fired persistent
15:54:00 fired volatile
```

Four fires were missed (15:50, 15:51, 15:52, 15:53). The persistent timer
produced **one** catch-up run, not four. The volatile timer produced none and
wrote no stamp file at any point.

Only `Persistent=true` creates
`~/.local/share/systemd/timers/stamp-<unit>.timer`. That file is the entire
mechanism.
