# -*- coding:utf-8 -*-


class Lab(object):
    """ 实验
    """

    def __init__(self, name, tags=[]):
        self.name = name
        # FIXME
        self._tags = list(tags)

    def insert_tag(self, tag):
        """ 插入标签，需要检查标签是否存在
        """
        # FIXME
        if tag not in self._tags:
            self._tags.append(tag)

    @property
    def tags(self):
        return self._tags[:]

    def can_be_started(self, user):
        """判断用户能否启动实验，只有登录的会员用户才能启动实验
        """
        # FIXME
        can = False
        if not user.is_authenticated:
            can = False
        elif user.is_member:
            can = True
        return can


tags = ["code", "score"]
l = Lab(name="shiyan", tags=tags)
l.insert_tag("boy")
l.insert_tag("boy")
print(l.tags)
print(tags)

