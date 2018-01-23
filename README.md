# wait-for-redis
Script to wait for Redis until it fully loaded https://github.com/antirez/redis/issues/4624

## Usage
```
./wait-for-redis.sh {redis host}:{redis port}
```

Example:
```
./wait-for-redis.sh localhost:6379
```
