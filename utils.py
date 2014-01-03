# -*- coding: utf-8 -*-

from flask import current_app

from flask import _request_ctx_stack as stack

from config import Config
from session import Session


session_cookie_name = 'SESSION_ID'
session_cookie_max_age = 7*24*3600

class Gae(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        app.teardown_request(self.teardown)
        app.after_request(self.after)

    def teardown(self, exception):
        self.app.logger.debug('Gae teardown')
        
        ctx = stack.top
        if hasattr(ctx, 'gae_config'):
            if ctx.gae_config.changed:
                self.app.logger.debug('save config')
                ctx.gae_config.save()

        #if hasattr(ctx, 'gae_session'):
        #    if ctx.gae_session.changed:
        #        self.app.logger.debug('Gae teardown, save session')
        #        ctx.gae_session.save()

    def after(self,resp):
        self.app.logger.debug('Gae after')
        ctx = stack.top
        if hasattr(ctx, 'gae_session'):
            if ctx.gae_session.changed:
                self.app.logger.debug('save session')
                session_id = ctx.gae_session.save()
            else:
                session_id = ctx.gae_session.get_session_id()
            
            if session_id:
                self.app.logger.debug('setting cookie %s:%s' % (session_cookie_name, session_id))
                resp.set_cookie(session_cookie_name, session_id, session_cookie_max_age)
            else:
                self.app.logger.debug('deleting cookie %s' % (session_cookie_name))
                resp.set_cookie(session_cookie_name,'', expires=0)


        return resp


    def get_config(self):
        self.app.logger.info('Gae loading config')
        return Config.get_global()


    def get_session(self,session_id):
        self.app.logger.info('Gae loading session')
        return Session.get_session(session_id)

    @property
    def config(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'gae_config'):
                ctx.gae_config = self.get_config()
            return ctx.gae_config

    @property
    def session(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'gae_session'):
                session_id = ctx.request.cookies.get(session_cookie_name)
                self.app.logger.debug('cookie %s = %s' % (session_cookie_name, session_id))
                ctx.gae_session = self.get_session(session_id)
            return ctx.gae_session





