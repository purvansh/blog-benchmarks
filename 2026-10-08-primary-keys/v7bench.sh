#!/usr/bin/env bash
export PGPASSWORD=bench
P="psql -h 127.0.0.1 -p 55432 -U postgres -d postgres -q -t -A -F|"
r() {
  $P -c "drop table if exists t;" >/dev/null
  $P -c "create table t (id uuid primary key, usr text not null, amount numeric(10,2) not null);" >/dev/null
  $P -c "checkpoint;" >/dev/null
  l0=$($P -c "select pg_current_wal_lsn();"); t0=$(date +%s.%N)
  $P -c "\copy t from '$PWD/$2.csv' with (format csv)" >/dev/null
  t1=$(date +%s.%N); l1=$($P -c "select pg_current_wal_lsn();")
  $P -c "select '$1', round($t1-$t0,2), pg_size_pretty(pg_relation_size('t_pkey')),
         (select round(avg_leaf_density::numeric,1) from pgstatindex('t_pkey')),
         pg_size_pretty('$l1'::pg_lsn - '$l0'::pg_lsn);"
}
printf "variant|copy_s|pk_index|leaf_density|wal\n"
r "v7 monotonic (no random tail)" uuid7mono
r "v7 at 10 ids/ms"               uuid7slow
r "v7 at 1000 ids/ms"             uuid7
r "v4 random"                     uuid4
