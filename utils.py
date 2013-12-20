# -*- coding: utf-8 -*-

from flask import current_app

from flask import _request_ctx_stack as stack

from config import Config

class Gae(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'gae_config'):
            if ctx.gae_config.changed:
                self.app.logger.debug('`Gae teardown, save config')
                ctx.gae_config.save()

    def get_config(self):
        self.app.logger.info('Gae loading config')
        return Config.get_global()

    @property
    def config(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'gae_config'):
                ctx.gae_config = self.get_config()
            return ctx.gae_config





