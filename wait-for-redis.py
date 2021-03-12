#!/usr/bin/env python

"""
Usage: python wait_for_redis.py REDISHOST:REDISPORT
"""

import socket, sys, time

address = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:6379"
host, port = address.split(":", 1)
port = int(port)

def entry_pairs(lines, prefix):
    """Extract lines "prefixkey:value" as ("key", "value") pairs."""
    for line in lines:
        if line.startswith(prefix):
            yield line[len(prefix):].split(":", 1)


print("Waiting for Redis at host {0}, port {1} to complete startup..."
      .format(host, port))
sys.stdout.flush()

# Wait for Redis to bind its port.

t0 = time.time()
while True:
    try:
        conn = socket.create_connection((host, port))
        break
    except socket.error:
        pass

    time.sleep(0.1)
    if time.time() > t0 + 1:
        t0 = time.time()
        print("Waiting for Redis to open listening socket.")
        sys.stdout.flush()

# Wait for Redis to complete loading.

while True:
    conn.sendall(b"info persistence\r\n")
    reply = b"".join(iter(lambda: conn.recv(1), b"\n"))
    if reply.startswith(b"-"):
        raise SystemExit("Redis: {0}.".format(reply.decode("utf-8").strip()))

    body = conn.recv(int(reply[1:]) + 2).decode("utf-8").splitlines()
    if "loading:0" in body:
        print("Redis reports loading completed.")
        sys.stdout.flush()
        break

    stats = dict(entry_pairs(body, "loading_"))
    if time.time() > t0 + 1:
        t0 = time.time()
        print("Redis loading dataset, loaded {0}% of {1:.3f} MB, eta {2} s.".format(
            stats.get("loaded_perc"), int(stats.get("total_bytes", 0.)) / 1024.0**2, stats.get("eta_seconds")))
        sys.stdout.flush()
    time.sleep(0.1)


print("Redis at host {0}, port {1} completed startup.".format(host, port))
sys.stdout.flush()
