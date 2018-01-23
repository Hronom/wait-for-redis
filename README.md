# wait-for-redis
Script to wait for Redis until it fully loaded https://github.com/antirez/redis/issues/4624

## Installation
This script uses `redis-tools`.

On Ubuntu install it using command:
```
RUN apt install redis-tools
```

## Usage
```
./wait-for-redis.sh {redis host}:{redis port}
```

Example:
```
./wait-for-redis.sh localhost:6379
```
