# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime
import logging

try: import simplejson as json
except ImportError: import json


Config_ancestor_key = ndb.Key('Configs','root')

class JsonProperty2(ndb.TextProperty):
    def _to_base_type(self, value):
        return json.dumps(value)

    def _from_base_type(self, value):
        return json.loads(value)


class Option(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()

class Config(ndb.Model):
    name = ndb.StringProperty()
    options = ndb.StructuredProperty(Option,repeated=True)






