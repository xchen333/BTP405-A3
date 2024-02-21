#!/bin/bash
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z -w 2 "$host" "$port"; do
  >&2 echo "Waiting for $host:$port..."
  sleep 2
done

>&2 echo "$host:$port is available, starting command $cmd"
exec $cmd
