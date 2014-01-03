# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime
import logging

try: import simplejson as json
except ImportError: import json

import uuid

from config import JsonProperty2


Session_ancestor_key = ndb.Key('Sessions','root')


class Session(ndb.Model):
    options = JsonProperty2()


    def __init__(self,**kwds):
        super(Session, self).__init__(**kwds)
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

    def clear(self):
        self.c = dict()
        self.changed = True

    def save(self):

        if (not self.c) and self.key:
            self.key.delete()
            logging.debug('no session data, sesssion removed')
            return None

        self.options = self.c
        self.put()
        logging.debug('session stored')
        return self.key.id()

    def get_session_id(self):
        if self.key:
            return self.key.id()
        return None


    @staticmethod
    def get_session(session_id=None):

        if session_id is not None:
            logging.debug('loading session %s' % session_id)
            c = Session.get_by_id(session_id, parent = Session_ancestor_key)
            if c is not None:
                logging.debug('session loaded')
                d = c.options
                if d is None:
                    c.options = dict()
                return c
            else:
                logging.debug('session not found')

        session_id = str(uuid.uuid4())
        logging.debug('allocated new session_id %s' % session_id)
        c = Session(id=session_id, parent = Session_ancestor_key)
        c.options = dict()
        return c





