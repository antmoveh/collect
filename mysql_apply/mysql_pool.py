
# pip  install  PyMySQL
# 為了兼容mysqldb，只需要加入
# pymysql.install_as_MySQLdb ()


import pymysql
conn = pymysql.connect(host = '127.0.0.1', user='root',  passwd="xxx",  db='mysql')
cur = conn.cursor()
cur.execute("SELECT Host,User FROM user")
for r in cur:
    print(r)
cur.close()
conn.close()

# orm 框架 SQLAlchemy 更django那套orm一样


# 连接池 pip install PyMysqlPool
# https://pypi.org/project/PyMysqlPool/

"""
file: new a mysql_config.py file and change to your db config
"""
db_config = {
    'local': {
        'host': "10.95.130.***", 'port': 8899,
        'user': "root", 'passwd': "****",
        'db': "marry", 'charset': "utf8",
        'pool': {
            #use = 0 no pool else use pool
            "use":1,
            # size is >=0,  0 is dynamic pool
            "size":0,
            #pool name
            "name":"local",
        }
    },
    'poi': {
        'host': "10.95.130.***", 'port': 8787,
        'user': "lujunxu", 'passwd': "****",
        'db': "poi_relation", 'charset': "utf8",
        'pool': {
            #use = 0 no pool else use pool
            "use":0,
            # size is >=0,  0 is dynamic pool
            "size":0,
            #pool name
            "name":"poi",
        }
    },
}


"""
Note:create your own table
"""
from PyMysqlPool.db_util.mysql_util import query,query_single,insertOrUpdate
import logging

"""
pool size special operation
"""
def query_pool_size():
    job_status = 2
    _sql = "select *  from master_job_list j  where j.job_status  in (%s) "
    _args = (job_status,)
    task = query(db_config['local'], _sql,_args)
    logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
    return

"""
single query
"""
def query_npool():
    job_status = 2
    _sql = "select *  from master_job_list j  where j.job_status  !=%s "
    _args = (job_status,)
    task = query_single(db_config['local'], _sql,_args)
    logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
    return

"""
insert
"""
def insert(nlp_rank_id,hit_query_word):
    #add more args
    _args = (nlp_rank_id,hit_query_word)
    _sql = """INSERT INTO nlp_rank_poi_online (nlp_rank_id,hit_query_word,rank_type,poi_list,poi_raw_list,article_id,city_id,status,create_time,version,source_from) VALUES (%s,%s,%s, %s, %s,%s, %s,%s, %s,%s,%s)"""
    affect = insertOrUpdate(db_config['local'], _sql, _args)
    logging.info("insert method insert result is %s ,input _data is %s ", affect , _args)
    return

"""
update
"""
def update(query_word,query_id):
    _args = (query_word,query_id)
    _sql = """update nlp_rank  set query_word = %s  WHERE  id = %s"""
    affect = insertOrUpdate(db_config['local'], _sql, _args)
    logging.info("update method update result is %s ,input _data is %s ", affect , _args)
    return


# 连接mysql cluster
"""
I have configured the server to use MySQL Cluster. The Cluster architecture is as follows:
One Cluster Manager(ip1)
Two Data Nodes (ip2,ip3)
Two SQL Nodes(ip4,ip5)
My Question: Which node should I use to connect from Python application?

You have to call SQL nodes from your application. Use comma separated ip addresses for this. In your code use DB_HOST = "ip4, ip5"
"""
