"""
Created on 2018-8-12.

A module of config center.
@author: chenwen9
"""
from flask.globals import g
import time
import datetime
import json
from json import JSONEncoder


class ConfItem(object):
    """Config center confitem class."""

    def __init__(self, project, name, value, parmhash=None, create_by=None, create_on=None, changed_by=None, changed_on=None):
        """The conitem init construction method."""
        self._project = project
        self.name = name
        self.value = value
        if not create_by:
            create_by = g.user.username
        self.create_by = create_by
        if not create_on:
            create_on = time.time()
        self.create_on = create_on
        if not changed_by:
            changed_by = g.user.username
        self.changed_by = changed_by
        if not changed_on:
            changed_on = time.time()
        self.changed_on = changed_on
        if not parmhash:
            parmhash = hash(self)
        self._hash = parmhash

    def gen_hash(self):
        self._hash = hash(self)

    def __eq__(self, other):
        return (
             self.__class__ == other.__class__ and
             self._project == other._project and
             self.name == other.name and
             self.value == other.value and
             self.create_by == other.create_by and
             self.create_on == other.create_on and
             self.changed_by == other.changed_by and
             self.changed_on == other.changed_on
        )

    def __hash__(self):
        return hash((self._project, self.name, self.value if isinstance(self.value, str) else json.dumps(self.value), \
                     self.create_by, self.create_on, self.changed_by, self.changed_on))

    def __repr__(self):
        if self._hash:
            return "cfg_%s_%s_%s" % (self._project, self.name, str(self._hash))
        else:
            return "cfg_%s_%s" % (self._project, self.name)

    def toJSON(self):
        return json.dumps(self, default=lambda o: {k: v for k, v in o.__dict__.items()} \
                          if not isinstance(o, datetime.datetime) else o.strftime('%Y-%m-%d %H:%M:%S.%f'),
            sort_keys=True)


class CustomJsonEncoder(JSONEncoder):
    """The flask redis customize json encoder, to generate obj to json str."""
    def default(self, obj):
        if isinstance(obj, ConfItem):
            return obj.__dict__
        return super(CustomJsonEncoder, self).encode(obj)
