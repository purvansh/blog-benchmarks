#!/usr/bin/env bash
export PGPASSWORD=bench
P="psql -h 127.0.0.1 -p 55432 -U postgres -d postgres -q -t -A -F|"
d() {
  $P -c "drop table if exists t;" >/dev/null
  $P -c "create table t (id $2 primary key, usr text not null, amount numeric(10,2) not null);" >/dev/null
  $P -c "\copy t from '$PWD/$3.csv' with (format csv)" >/dev/null
  $P -c "select '$1', leaf_pages, round(avg_leaf_density::numeric,1), round(leaf_fragmentation::numeric,1) from pgstatindex('t_pkey');"
}
printf "scheme|leaf_pages|avg_leaf_density_pct|leaf_fragmentation_pct\n"
d seq       bigint seq
d snowflake bigint snowflake
d uuid7     uuid   uuid7
d uuid4     uuid   uuid4
d ulid      text   ulid
d nanoid    text   nanoid
d uuid4text text   uuid4text
