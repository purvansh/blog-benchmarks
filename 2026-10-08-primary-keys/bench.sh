#!/usr/bin/env bash
# 1,000,000 identical payload rows per scheme. Only the primary key differs.
# Measured: COPY wall clock, heap size, primary key index size, and WAL bytes
# written during the load. A CHECKPOINT before each run makes the full page
# write behaviour comparable instead of depending on where the last one landed.
set -uo pipefail
export PGPASSWORD=bench
PSQL="psql -h 127.0.0.1 -p 55432 -U postgres -d postgres -q -t -A -F|"

row() {
  local name="$1" type="$2" csv="$3"
  $PSQL -c "drop table if exists t;" >/dev/null
  $PSQL -c "create table t (id $type primary key, usr text not null, amount numeric(10,2) not null);" >/dev/null
  $PSQL -c "checkpoint;" >/dev/null
  local lsn0 t0 t1 lsn1
  lsn0=$($PSQL -c "select pg_current_wal_lsn();")
  t0=$(date +%s.%N)
  $PSQL -c "\copy t from '$csv' with (format csv)" >/dev/null
  t1=$(date +%s.%N)
  lsn1=$($PSQL -c "select pg_current_wal_lsn();")
  $PSQL -F'|' -c "
    select
      '$name',
      round($t1 - $t0, 2),
      pg_size_pretty(pg_relation_size('t')),
      pg_size_pretty(pg_relation_size('t_pkey')),
      pg_relation_size('t_pkey'),
      pg_size_pretty('$lsn1'::pg_lsn - '$lsn0'::pg_lsn),
      ('$lsn1'::pg_lsn - '$lsn0'::pg_lsn);"
}

printf "scheme|copy_s|heap|pk_index|pk_bytes|wal|wal_bytes\n"
row seq       bigint "$PWD/seq.csv"
row snowflake bigint "$PWD/snowflake.csv"
row uuid7     uuid   "$PWD/uuid7.csv"
row uuid4     uuid   "$PWD/uuid4.csv"
row ulid      text   "$PWD/ulid.csv"
row nanoid    text   "$PWD/nanoid.csv"
row uuid4text text   "$PWD/uuid4text.csv"
