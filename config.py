# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime
import logging

try: import simplejson as json
except ImportError: import json


Config_ancestor_key = ndb.Key('Configs','root')
Config_key = 'global'

class JsonProperty2(ndb.TextProperty):
    def _to_base_type(self, value):
        return json.dumps(value)

    def _from_base_type(self, value):
        return json.loads(value)


class Config(ndb.Model):
    options = JsonProperty2()


    def __init__(self,**kwds):
        super(Config, self).__init__(**kwds)
        self.changed = False
        self.c = None

    def __delitem__(self, key):
        if self.c is None:
            self.c = self.options
        self.changed = True
        del self.c[key]        

    def __setitem__(self, key, value):
        if self.c is None:
            self.c = self.options

        self.changed = True
        self.c[key]=value

    def __getitem__(self, key):
        if self.c is None:
            self.c = self.options
        return self.c[key]


    def save(self):
        self.options = self.c
        self.put()

    @staticmethod
    def get_global():
        c = Config.get_or_insert(Config_key,parent = Config_ancestor_key)
        d = c.options
        if d is None:
            c.options = dict()
        return c






