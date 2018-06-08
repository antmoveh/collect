from typing import Dict, List, Tuple


class Project(object):

    def __init__(self):
        if not hasattr(Project, 'db'):
            Project.create_pool()
        self._db = Project.db

    @staticmethod
    def create_pool():
        pool = """create connect pool"""
        db = pool.collectname
        db.authenticate("username", "password")
        Project.db = db

    def common_operation_mongo(self, collection: str, curd: str, kwargs: Dict =None,
                               _query: Dict[str, str] = None,
                               _just_one: str ="false",
                               _upsert: bool = False,
                               _multi: bool = False,
                               _inclusion: Dict[str, int] =None,
                               _sort: List[Tuple[str, int]] =None,
                               _skip: int =0,
                               _limit: int =10,
                               _all: bool =False):
        """
        :param collection: database name
        :param curd: insert|remove|update|find
        :param kwargs: insert or update dict
        :param _query: query params
        :param _just_one: delete one if true
        :param _inclusion: filter params
        :param _sort: sorted params
        :param _skip:
        :param _limit:
        :param _upsert: add new record if no match
        :param _multi: update more than one
        :param _all: return all data if True
        :return: different data with curd  str|dict|list
        """
        if curd == "insert":
            _kwargs = kwargs
            res = self._db.get_collection(collection).insert(_kwargs)
            return str(res)
        if curd == "remove":
            res = self._db.get_collection(collection).remove(_query, _just_one)
            return res
        if curd == "find":
            if _all:
                res = self._db.get_collection(collection).find(_query, _inclusion)
            else:
                res = self._db.get_collection(collection).find(_query, _inclusion).sort(_sort).skip(_skip).limit(_limit)
            return {"list": list(res), "total": res.count()}
        if curd == "find_one":
            res = self._db.get_collection(collection).find_one(_query, _inclusion)
            return res
        if curd == "update":
            _update = kwargs
            res = self._db.get_collection(collection).update(_query, _update, upsert=_upsert, multi=_multi)
            return res
