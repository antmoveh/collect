from redis.sentinel import Sentinel

redis_sentinels = [("127.0.0.1", 26379), ("127.0.0.1", 26380), ("127.0.0.1", 26381)]
redis_host = [("master", 6379), ("slave0", 6380), ("slave1", 6381)]


sent = Sentinel(redis_sentinels, socket_timeout=0.1)
master = sent.master_for('mymaster', socket_timeout=0.1)
master.set('foo', 'bar')
slave = sent.slave_for('mymaster', socket_timeout=0.1)
slave.get('foo')

# 高可用测试
"""
import time
while True:
    sentinel = Sentinel([('127.0.0.1', 26379),('127.0.0.1', 26380)], socket_timeout=0.1)
    time.sleep(0.5)
    print(sentinel.discover_master('mymaster'))
    print(sentinel.discover_slaves('mymaster'))
    master = sentinel.master_for('mymaster', socket_timeout=0.1)
    print(master.set('foo', 'bar'))
    print(master.get('foo'))
    slave = sentinel.slave_for('mymaster', socket_timeout=0.1)
    slave.get('foo')
发生主从切换时，业务大概会有1-2s的中断后恢复正常。
当哨兵挂掉一个时（两个哨兵），业务无感知，但是是建立在主从不会切换的情况下（此时一个哨兵无法完成故障转移）。
"""

# 哨兵连接池
from redis.connection import PythonParser
import redis
if redis_sentinels:
    from redis.sentinel import SentinelConnectionPool
    service_name = "mymaster"
    sentinel = Sentinel(sentinels=redis_sentinels, password='redis_password' or None, socket_timeout=0.5)
    pool = SentinelConnectionPool(service_name, sentinel,
                                  db=15,
                                  parser_class=PythonParser)
else:
    from redis.connection import ConnectionPool
    pool = ConnectionPool(host="127.0.0.1",
                          port="6379",
                          password='redis_password' or None,
                          db=15,
                          parser_class=PythonParser)

REDIS = redis.StrictRedis(connection_pool=pool)


# the second
def test_slave_round_robin():
    sentinel = Sentinel(sentinels=redis_sentinels, password='redis_password' or None, socket_timeout=0.5)
    pool = SentinelConnectionPool('mymaster', sentinel)
    rotator = pool.rotate_slaves()
    assert next(rotator) in redis_host
    assert next(rotator) in redis_host
    # Fallback to master
    assert next(rotator) == redis_host[0]  # master node

