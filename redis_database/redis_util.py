import redis

redis_pool = None


def init_redis():
    global redis_pool
    if not redis_pool:
        redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

def get_connection():
    global redis_pool
    init_redis()
    return redis.Redis(connection_pool=redis_pool)


def list_push(key, value):
    r = get_connection()
    r.rpush(key, value)


def list_push_left(key, value):
    r = get_connection()
    r.lpush(key, value)


def list_push_lists(key, value):
    r = get_connection()
    for v in value:
        r.rpush(key, v)


def list_pop(key):
    r = get_connection()
    return r.lpop(key)


def llendb(key):
    r = get_connection()
    return r.llen(key)
