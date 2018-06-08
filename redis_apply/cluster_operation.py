# redis cluster的nodes
REDIS_NODES = [
    {"host": "127.0.0.1", "port": 7000},
    {"host": "127.0.0.1", "port": 7001},
    {"host": "127.0.0.1", "port": 7002},
    {"host": "127.0.0.1", "port": 7003},
    {"host": "127.0.0.1", "port": 7004},
    {"host": "127.0.0.1", "port": 7005},
]

# redis的key的过期时间,单位s
REDIS_EXPIRETIME = 1200
REDIS_MAX_CONNECTIONS = 50
REDIS_PASSWD = 'CATAPI'

import redis
from rediscluster import StrictRedisCluster

redisClient = StrictRedisCluster(startup_nodes=REDIS_NODES, max_connections=REDIS_MAX_CONNECTIONS, password=REDIS_PASSWD)
redisClient.set('testkey', 12, 10)
redisClient.incr('testkey', 13)
print(redisClient.get('testkey'))


#
def get_redis_client(redis_type='single', host='127.0.0.1', port=6379, db=0, pwd=None, nodes=None, timeout=3):
    if redis_type == 'single':
        pool = redis.ConnectionPool(host=host, port=port, db=db, password=pwd, socket_timeout=timeout, socket_connect_timeout=timeout, encoding='utf-8', decode_responses=True)
        client = redis.StrictRedis(connection_pool=pool)
    else:
        client = StrictRedisCluster(startup_nodes=nodes, decode_responses=True, socket_timeout=timeout, socket_connect_timeout=timeout)
    return client