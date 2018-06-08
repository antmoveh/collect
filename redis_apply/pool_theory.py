import redis

rdp = redis.ConnectionPool(host="127.0.0.1", port=6379, password="x")
rdc = redis.StrictRedis(connection_pool=rdp)

rdc.set("name", "Y")
rdc.get("name")

"""
当redis.ConnectionPool 实例化的时候, 做了什么

def __init__(self, connection_class=Connection, max_connections=None,
                 **connection_kwargs):
        max_connections = max_connections or 2 ** 31
        if not isinstance(max_connections, (int, long)) or max_connections < 0:
            raise ValueError('"max_connections" must be a positive integer')

        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.max_connections = max_connections
这个连接池的实例化其实未做任何真实的redis连接, 仅仅是设置最大连接数, 连接参数和连接类

StrictRedis 实例化的时候, 又做了什么
 def __init__(self, ...connection_pool=None...):
        if not connection_pool:
            ...
            connection_pool = ConnectionPool(**kwargs)
        self.connection_pool = connection_pool
以上仅保留了关键部分代码
可以看出, 使用StrictRedis 即使不创建连接池, 他也会自己创建
到这里, 我们还没有看到什么redis连接真实发生

下一步就是set 操作了, 很明显, 这个时候一定会发生redis连接(要不然怎么set)
def set(self, name, value, ex=None, px=None, nx=False, xx=False):
    ...
    return self.execute_command('SET', *pieces)
    
我们继续看看execute_command
 def execute_command(self, *args, **options):
        "Execute a command and return a parsed response"
        pool = self.connection_pool
        command_name = args[0]
        connection = pool.get_connection(command_name, **options)
        try:
            connection.send_command(*args)
            return self.parse_response(connection, command_name, **options)
        except (ConnectionError, TimeoutError) as e:
            connection.disconnect()
            if not connection.retry_on_timeout and isinstance(e, TimeoutError):
                raise
            connection.send_command(*args)
            return self.parse_response(connection, command_name, **options)
        finally:
            pool.release(connection)
终于, 在这我们看到到了连接创建

connection = pool.get_connection(command_name, **options)
这里调用的是ConnectionPool的get_connection
def get_connection(self, command_name, *keys, **options):
        "Get a connection from the pool"
        self._checkpid()
        try:
            connection = self._available_connections.pop()
        except IndexError:
            connection = self.make_connection()
        self._in_use_connections.add(connection)
        return connection
        
如果有可用的连接, 获取可用的链接, 如果没有, 创建一个
def make_connection(self):
        "Create a new connection"
        if self._created_connections >= self.max_connections:
            raise ConnectionError("Too many connections")
        self._created_connections += 1
        return self.connection_class(**self.connection_kwargs)
终于, 我们看到了, 在这里创建了连接
在ConnectionPool的实例中, 有两个list, 依次是_available_connections, _in_use_connections,
分别表示可用的连接集合和正在使用的连接集合, 在上面的get_connection中, 我们可以看到获取连接的过程是

从可用连接集合尝试获取连接,
如果获取不到, 重新创建连接
将获取到的连接添加到正在使用的连接集合
上面是往_in_use_connections里添加连接的, 这种连接表示正在使用中, 那是什么时候将正在使用的连接放回到可用连接列表中的呢

这个还是在execute_command里, 我们可以看到在执行redis操作时, 在finally部分, 会执行一下
pool.release(connection)
连接池对象调用release方法, 将连接从_in_use_connections 放回 _available_connections, 这样后续的连接获取就能再次使用这个连接了
release 方法如下
 def release(self, connection):
        "Releases the connection back to the pool"
        self._checkpid()
        if connection.pid != self.pid:
            return
        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)

至此, 我们把连接池的管理流程走了一遍, ConnectionPool通过管理可用连接列表(_available_connections) 和 正在使用的连接列表 从而实现连接池管理
"""