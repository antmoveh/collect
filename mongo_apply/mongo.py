
import pymongo
from pymongo import MongoClient

# pool
client = MongoClient("localhost", "27017")
# client = pymongo.MongoClient("mongodb://localhost:27017")
# client = MongoClient(host=None, port=None)
# client = MongoClient(host=None, port=None, maxPoolSize=200)
# client = MongoClient(host=None, port=None, maxPoolSize=None)
# client = MongoClient(host=None, port=None, maxPoolSize=50, waitQueueMultiple=10)
# client = MongoClient(host=None, port=None, waitQueueTimeoutMs=100)
db = client.dbname or client["dbname"]

# replica set
config = {"_id": "foo", "members": [
    {"_id": 0, "host": "localhost: 27017"},
    {"_id": 1, "host": "localhost: 27018"},
    {"_id": 2, "host": "localhost: 27019"},
]}
# 连接任意节点，自动感知主节点
repl = MongoClient("localhost", replicaset="foo")
# repl = MongoClient("localhost:27018", replicaset="foo")
# repl = MongoClient("localhost", 27019, replicaset="foo")
# repl = MongoClient("mongodb://localhost:27017,localhost:27018/?replicaSet=foo")
db2 = repl.test

# secondary Reads
client = MongoClient("localhost:27017", replicaSet="foo", readPreference="secondaryPreferred")
client.read_preference

from pymongo import ReadPreference
db3 = client.get_database("test", read_preference=ReadPreference.SECONDARY)
coll = db.get_collection("test", read_preference=ReadPreference.PRIMARY)
coll2 = coll.with_options(read_preference=ReadPreference.NEAREST)
"""
PRIMARY: Read from the primary. This is the default read preference, and provides the strongest consistency. If no primary is available, raise AutoReconnect.
PRIMARY_PREFERRED: Read from the primary if available, otherwise read from a secondary.
SECONDARY: Read from a secondary. If no matching secondary is available, raise AutoReconnect.
SECONDARY_PREFERRED: Read from a secondary if available, otherwise from the primary.
NEAREST: Read from any available member.
"""
# tag sets
from pymongo.read_preferences import Secondary
db4 = client.get_database("test", read_preference=Secondary([{"dc": "ny"}, {"dc": "sf"}]))
# local threshold
client = pymongo.MongoClient(replicaSet="rep10", readPreference="secondaryPreferred", localThresholdMS=35)

# mongos
lient = MongoClient('mongodb://host1,host2,host3/?localThresholdMS=30')
# Warning Do not connect PyMongo to a pool of mongos instances through a load balancer. A single socket connection must always be routed to the same mongos instance for proper cursor support.