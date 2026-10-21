#!/usr/bin/env bash
echo "$(date -Iseconds) fired $1" >> "$(dirname "$0")/fires.log"
