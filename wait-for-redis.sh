#!/usr/bin/env bash

hostport=(${1//:/ })
HOST=${hostport[0]}
PORT=${hostport[1]}

echo "Start waiting for Redis fully start. Host '$HOST', '$PORT'..."
echo "Try ping Redis... "
PONG=`redis-cli -h $HOST -p $PORT ping | grep PONG`
while [ -z "$PONG" ]; do
    sleep 1
    echo -n "Retry Redis ping... "
    PONG=`redis-cli -h $HOST -p $PORT ping | grep PONG`
done
echo "Redis at host '$HOST', port '$PORT' fully started."
