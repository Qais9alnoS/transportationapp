import os
import redis
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def cache_get(key):
    value = redis_client.get(key)
    if value is not None:
        try:
            return json.loads(value)
        except Exception:
            return value
    return None

def cache_set(key, value, ttl=300):
    try:
        redis_client.set(key, json.dumps(value), ex=ttl)
    except Exception:
        pass

def delete_pattern(pattern):
    for key in redis_client.scan_iter(match=pattern):
        redis_client.delete(key)

__all__ = ["cache_get", "cache_set", "redis_client", "delete_pattern"] 