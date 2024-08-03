from datetime import datetime, timezone
import os
import json
import time
import uuid
from cachetools import cached, TTLCache

# Generate a UUID once at startup
BOOT_UUID = str(uuid.uuid4())

# Create a cache with a Time-To-Live (TTL) of 1 hour
cache = TTLCache(maxsize=1, ttl=86400)


@cached(cache)
def get_cached_time():
    """Returns the current time, cached for one hour."""
    return datetime.now(tz=timezone.utc).isoformat()

def endpoint():
    current_time = get_cached_time()
    pid = os.getpid()
    
    response = {
        'time': current_time,
        'pid': pid,
        'uuid': BOOT_UUID
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
