import redis


class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host='localhost', port=6379)
        self.channel = 'monitor'

    def publish(self, msg):
        self.__conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub


# obj = RedisHelper()
# obj.publish('hello')
#
# redis_sub = obj.subscribe()
# while True:
#     msg = redis_sub.parse_response()
#     print(msg)


pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.StrictRedis(connection_pool=pool)
# String 操作
# r.set("name", "zhangsan")
# r.setex("name", "zz", 10)
# r.psetex("name", time_ms=100, value="zd")
# r.mset(name1="zhangsan", name2="lisi")
# r.mget({"name1": "zhangsan", "name2": "lisi"})
# print(r.get("name"))
# print(r.mget("name1", "name2"))
# li = ["name1", "name2"]
# print(r.mget(li))
# print(r.getset("name1", "wangwu"))
# print(r.get("name1"))
# print(r.getrange("name", 0, 3))
# r.setrange("name", 1, "z")
# r.setrange("name", 6, "zzzzzzz")
# str = "345"
# r.set("name", str)
# for i in str:
#     print(i, ord(i), bin(ord(i)))
# r.setbit("name", 6, 0)
# print(r.get("name"))
# r.set("name", "3")
# print(r.getbit("name", 5))
# print(r.getbit("name", 6))
# r.set("name", "345")
# print(r.bitcount("name", start=0, end=1))
# r.set("name", "zhangsan")
# print(r.strlen("name"))
# print(r.incr("mount", amount=2))
# print(r.incr("mount"))
# print(r.incr("mount", amount=3))
# print(r.incr("mount", amount=6))
# print(r.get("mount"))
# print(r.incrbyfloat("m", amount=1.0))
# print(r.incrbyfloat("m"))
# print(r.decr("mount", amount=1))
# r.set("name", "zhangsan")
# print(r.get("name"))
# r.append("name", "lisi")
# print(r.get("name"))


# Hash 操作
# r.hset('dic_name', 'a1', 'aa')
# dic = {'a1': 'aa', 'b1': 'bb'}
# r.hmset('dic_name', dic)
# li = ['a1', 'b1']
# print(r.hget('dic_name', 'a1'))
# print(r.hget('dic_name', 'b1'))
# print(r.hmget("dic_name", li))
# print(r.hmget("dic_name", "a1", "b1"))
# print(r.hgetall('dic_name'))
# print(r.hlen("dic_name"))
# print(r.hkeys("dic_name"))
# print(r.hvals("dic_name"))
# print(r.keys())
# print(r.hexists("dic_name", "a1"))
# r.hdel("dic_name", "a1")
# print(r.hincrby("demo", "a", amount=2))
# print(r.hincrbyfloat("demo", "b", amount=1.0))


# List 操作
# r.lpush("list_name", 2)
# r.lpush("list_name", 3, 4, 5)
# r.rpush("list_name", 2, 3, 4, 5)
# r.rpushx("list_name", 0)
# r.lpushx("list_name", 0)
# r.linsert("list_name", "BEFORE", "2", "SS")
# r.lset("list_name", 0, "bbb")
# #r.lrem("list_name", "SS", num=0)
# print(r.lpop("list_name"))
# print(r.rpop("list_name"))
# print(r.lindex("list_name", 1))
# print(r.lrange("list_name", 0, -1))
# print(r.ltrim("list_name", 0, 2))
# r.rpoplpush("list_name", "list_name1")
# r.brpoplpush("list_name", "list_name1", timeout=0)
# r.lpush("list_name", 3, 4, 5)
# r.lpush("list_name1", 3, 4, 5)
# print(r.llen("list_name"))
# while True:
#     print(r.blpop(["list_name", "list_name1"], timeout=0))
#     print(r.brpop(["list_name", "list_name1"], timeout=0))
#     print(r.lrange("list_name", 0, -1), r.lrange("list_name1", 0, -1))


# Set 操作
# r.sadd("set_name", "aa")
# r.sadd("set_name", "aa", "bb")
# print(r.smembers("set_name"))
# print(r.scard("set_name"))
# r.sadd("set_name", "aa", "bb")
# r.sadd("set_name1", "bb", "cc")
# r.sadd("set_name2", "bb", "cc", "dd")
# print(r.sdiff("set_name", "set_name1", "set_name2"))
# r.sdiffstore("set_name3", "set_name", "set_name1", "set_name2")
# print(r.sinter("set_name", "set_name1", "set_name2"))
# r.sinterstore("set_name3", "set_name", "set_name1", "set_name2")
# print(r.sismember("set_name", "aa"))
# r.smove("set_name2", "set_name", "dd")
# print(r.spop("set_name"))
# print(r.srandmember("set_name2", 2))
# print(r.srem("set_name2", "bb", "dd"))
# print(r.sunion("set_name", "set_name1", "set_name2"))
# r.sunionstore("set_name4", "set_name", "set_name1", "set_name2")


# 有序集合
# r.zadd("zset_name", "a1", 6, "a2", 2, "a3", 5)
# r.zadd("zset_name1", a1=7, b1=10, b2=5)
# print(r.zcard("zset_name"))
# print(r.zcount("zset_name", 1, 5))
# r.zincrby("zset_name", "a1", amount=2)
# aa = r.zrange("zset_name", 0, 1, desc=False, withscores=True, score_cast_func=int)
# print(aa)
# print(r.zrank("zset_name", "a2"))
# print(r.zrevrank("zset_name", "a2"))
# print(r.zscore("zset_name", "a1"))
# r.zrem("zset_name", "a1", "a2")
# r.zremrangebyrank("zset_name", 0, 1)
# r.zremrangebyscore("zset_name", 2, 5)
# r.zinterstore("zset_name2", ("zset_name1", "zset_name"), aggregate="MAX")
# print(r.zscan("zset_name2"))
# r.zunionstore("zset_name2", ("zset_name1", "zset_name"), aggregate="MAX")
# print(r.zscan("zset_name2"))


# import datetime
# 其他常用操作
# print(r.delete("name"))
# print(r.exists("demo"))
# print(r.keys(pattern='*'))
# print(r.expire("demo", 6))
# print(r.rename("set_name", "set_name7"))
# print(r.move("set_name2", 1))
# print(r.randomkey())
# print(r.type("zset_name"))